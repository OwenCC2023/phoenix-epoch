"""
Policy effects helper module.

Provides functions to:
  - Merge all active policy effects for a nation (context-dependent on government/traits)
  - Validate policy changes against requirements and cross-policy bans
  - Determine which buildings and units are blocked by current policies
"""

from .policy_constants import (
    POLICY_CATEGORIES,
    POLICY_EFFECTS,
    POLICY_REQUIREMENTS,
    POLICY_BANS,
    BUILDING_POLICY_REQUIREMENTS,
    BUILDING_POLICY_BANS,
    UNIT_POLICY_REQUIREMENTS,
    UNIT_POLICY_BANS,
)


def get_nation_policy_effects(nation):
    """
    Iterate NationPolicy rows, look up POLICY_EFFECTS, apply government/trait
    modifiers, and merge all effects additively.

    Returns a flat dict of effect_key -> value.  ``building_efficiency_bonus``
    values are dicts (category -> bonus) and are merged by category key.

    Same merge pattern as ``get_nation_trait_effects()`` in ``nations/helpers.py``.
    """
    from .models import NationPolicy

    gov_values = {
        nation.gov_direction,
        nation.gov_economic_category,
        nation.gov_structure,
        nation.gov_power_origin,
        nation.gov_power_type,
    }

    # Collect the nation's trait keys (strong + weak)
    traits = nation.ideology_traits or {}
    nation_traits = set()
    strong = traits.get("strong")
    if strong:
        nation_traits.add(strong)
    for w in traits.get("weak", []):
        nation_traits.add(w)

    merged = {}
    policies = NationPolicy.objects.filter(nation=nation)

    for policy in policies:
        cat = policy.category
        level = policy.level

        cat_effects = POLICY_EFFECTS.get(cat)
        if not cat_effects:
            continue
        level_effects = cat_effects.get(level)
        if not level_effects:
            continue

        # Layer 1: base effects
        _merge_into(merged, level_effects.get("base", {}))

        # Layer 2: government modifiers — applies all matching axis values
        gov_mods = level_effects.get("government_modifiers", {})
        for axis_val, mods in gov_mods.items():
            if axis_val in gov_values:
                _merge_into(merged, mods)

        # Layer 3: trait modifiers (all matching traits)
        trait_mods = level_effects.get("trait_modifiers", {})
        for trait_key in nation_traits:
            if trait_key in trait_mods:
                _merge_into(merged, trait_mods[trait_key])

    return merged


def _merge_into(target, source):
    """
    Merge source effects into target additively.

    Handles ``building_efficiency_bonus`` as a nested dict of category -> bonus.
    All other keys are treated as numeric and summed.
    """
    for key, value in source.items():
        if key == "building_efficiency_bonus":
            if key not in target:
                target[key] = {}
            for cat, bonus in value.items():
                target[key][cat] = target[key].get(cat, 0.0) + bonus
        else:
            target[key] = target.get(key, 0.0) + value


def validate_policy_change(nation, category, new_level):
    """
    Check POLICY_REQUIREMENTS and POLICY_BANS for a proposed policy change.

    POLICY_REQUIREMENTS keys:
      ``gov_axis_required``   — nation must have at least one of these axis values
      ``gov_axis_banned``     — nation must not have any of these axis values
      ``traits_required``     — nation must have at least one of these traits
      ``traits_banned``       — nation must not have any of these traits
      ``policies_required``   — list of (category, min_level) tuples

    Returns a list of error strings.  Empty list means the change is valid.
    """
    from .models import NationPolicy

    errors = []
    gov_values = {
        nation.gov_direction,
        nation.gov_economic_category,
        nation.gov_structure,
        nation.gov_power_origin,
        nation.gov_power_type,
    }

    # Collect nation's trait keys
    traits = nation.ideology_traits or {}
    nation_traits = set()
    strong = traits.get("strong")
    if strong:
        nation_traits.add(strong)
    for w in traits.get("weak", []):
        nation_traits.add(w)

    # Check requirements for the target level
    req = POLICY_REQUIREMENTS.get((category, new_level))
    if req:
        # Government axis checks
        required = req.get("gov_axis_required")
        if required and not gov_values.intersection(required):
            errors.append(
                f"Policy {category} level {new_level} requires one of "
                f"government axis values: {', '.join(required)}"
            )

        banned = req.get("gov_axis_banned")
        if banned and gov_values.intersection(banned):
            bad = gov_values.intersection(banned)
            errors.append(
                f"Policy {category} level {new_level} is banned for "
                f"government axis values: {', '.join(bad)}"
            )

        # Trait checks
        traits_required = req.get("traits_required")
        if traits_required:
            if not nation_traits.intersection(traits_required):
                errors.append(
                    f"Policy {category} level {new_level} requires one of "
                    f"traits: {', '.join(traits_required)}"
                )

        traits_banned = req.get("traits_banned")
        if traits_banned:
            bad = nation_traits.intersection(traits_banned)
            if bad:
                errors.append(
                    f"Policy {category} level {new_level} is banned for "
                    f"traits: {', '.join(bad)}"
                )

        # Prerequisite policies
        policies_required = req.get("policies_required")
        if policies_required:
            current_policies = dict(
                NationPolicy.objects.filter(nation=nation)
                .values_list("category", "level")
            )
            for req_cat, min_level in policies_required:
                current = current_policies.get(req_cat, 0)
                if current < min_level:
                    errors.append(
                        f"Policy {category} level {new_level} requires "
                        f"{req_cat} >= {min_level} (currently {current})"
                    )

    # Check cross-policy bans
    # Get the nation's current policy levels (excluding the category being changed)
    current_policies = dict(
        NationPolicy.objects.filter(nation=nation)
        .exclude(category=category)
        .values_list("category", "level")
    )

    # Check if any existing policy bans the new level
    for (ban_cat, ban_level), banned_list in POLICY_BANS.items():
        # If this nation currently has (ban_cat, ban_level), check if our
        # proposed (category, new_level) is in the banned list.
        if ban_cat == category:
            continue  # same category — can't ban yourself
        current = current_policies.get(ban_cat)
        if current is not None and current == ban_level:
            for banned_cat, banned_level in banned_list:
                if banned_cat == category and banned_level == new_level:
                    cat_def = POLICY_CATEGORIES.get(ban_cat, {})
                    ban_level_name = ""
                    levels = cat_def.get("levels", [])
                    if ban_level < len(levels):
                        ban_level_name = levels[ban_level].get("name", "")
                    errors.append(
                        f"Policy {category} level {new_level} is banned by "
                        f"current policy {ban_cat}: {ban_level_name}"
                    )

    # Also check if the new level would ban any existing policy
    bans_from_new = POLICY_BANS.get((category, new_level), [])
    for banned_cat, banned_level in bans_from_new:
        if banned_cat == category:
            continue  # same category
        current = current_policies.get(banned_cat)
        if current is not None and current == banned_level:
            cat_def = POLICY_CATEGORIES.get(banned_cat, {})
            level_name = ""
            levels = cat_def.get("levels", [])
            if banned_level < len(levels):
                level_name = levels[banned_level].get("name", "")
            errors.append(
                f"Policy {category} level {new_level} conflicts with "
                f"current policy {banned_cat}: {level_name}"
            )

    return errors


def get_policy_building_blocks(nation):
    """
    Return the set of building_types blocked by the nation's current policies.

    Checks BUILDING_POLICY_REQUIREMENTS (all must be met — AND logic) and
    BUILDING_POLICY_BANS (any match blocks).
    """
    from .models import NationPolicy

    current_policies = dict(
        NationPolicy.objects.filter(nation=nation)
        .values_list("category", "level")
    )

    blocked = set()

    # Requirements: all (category, min_level) must be met
    for building_type, requirements in BUILDING_POLICY_REQUIREMENTS.items():
        for req_cat, min_level in requirements:
            current = current_policies.get(req_cat, 0)
            if current < min_level:
                blocked.add(building_type)
                break

    # Bans: any (category, exact_level) match blocks
    for building_type, bans in BUILDING_POLICY_BANS.items():
        for ban_cat, ban_level in bans:
            current = current_policies.get(ban_cat)
            if current is not None and current == ban_level:
                blocked.add(building_type)
                break

    return blocked


def get_policy_unit_blocks(nation):
    """
    Return the set of unit_types blocked by the nation's current policies.

    Checks UNIT_POLICY_REQUIREMENTS (all must be met — AND logic) and
    UNIT_POLICY_BANS (any match blocks).
    """
    from .models import NationPolicy

    current_policies = dict(
        NationPolicy.objects.filter(nation=nation)
        .values_list("category", "level")
    )

    blocked = set()

    # Requirements: all (category, min_level) must be met
    for unit_type, requirements in UNIT_POLICY_REQUIREMENTS.items():
        for req_cat, min_level in requirements:
            current = current_policies.get(req_cat, 0)
            if current < min_level:
                blocked.add(unit_type)
                break

    # Bans: any (category, exact_level) match blocks
    for unit_type, bans in UNIT_POLICY_BANS.items():
        for ban_cat, ban_level in bans:
            current = current_policies.get(ban_cat)
            if current is not None and current == ban_level:
                blocked.add(unit_type)
                break

    return blocked
