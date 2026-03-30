"""
Policy effects helper module.

Provides functions to:
  - Merge all active policy effects for a nation (context-dependent on government/traits)
  - Apply gov-policy multiplier (24×277 matrix)
  - Validate policy changes against requirements, cross-policy bans, and disabling cascade
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
from .gov_policy_multipliers import GOV_POLICY_MULTIPLIERS
from .disabling_rules import (
    TRAIT_POLICY_DISABLES,
    GOV_POLICY_DISABLES,
    POLICY_POLICY_DISABLES,
)
from .policy_building_forbidden import POLICY_BUILDING_FORBIDDEN
from .security_policy_data import SECURITY_POLICY_MULTIPLIERS


def get_nation_policy_effects(nation):
    """
    Iterate NationPolicy rows, look up POLICY_EFFECTS, apply government/trait
    modifiers, compute the gov-policy multiplier, and merge all effects additively.

    Returns a flat dict of effect_key -> value.  ``building_efficiency``
    values are dicts (category -> bonus) and are merged by category key.

    Gov-policy multiplier: each of the nation's 5 gov components may scale
    a policy's effects. The combined multiplier is the product of all 5
    component multipliers, clamped to [0.1, 5.0].
    """
    from .models import NationPolicy

    gov_values = {
        nation.gov_direction,
        nation.gov_economic_category,
        nation.gov_structure,
        nation.gov_power_origin,
        nation.gov_power_type,
    }
    gov_components = [
        nation.gov_direction,
        nation.gov_economic_category,
        nation.gov_structure,
        nation.gov_power_origin,
        nation.gov_power_type,
    ]

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

        # Compute combined gov-policy multiplier for this (category, level)
        multiplier = _compute_gov_policy_multiplier(gov_components, cat, level)

        # Layer 1: base effects (scaled by multiplier)
        base = level_effects.get("base", {})
        if base:
            _merge_into(merged, _scale_effects(base, multiplier))

        # Layer 2: government modifiers — applies all matching axis values
        gov_mods = level_effects.get("government_modifiers", {})
        for axis_val, mods in gov_mods.items():
            if axis_val in gov_values:
                _merge_into(merged, _scale_effects(mods, multiplier))

        # Layer 3: trait modifiers (all matching traits)
        trait_mods = level_effects.get("trait_modifiers", {})
        for trait_key in nation_traits:
            if trait_key in trait_mods:
                _merge_into(merged, _scale_effects(trait_mods[trait_key], multiplier))

    return merged


def _compute_gov_policy_multiplier(gov_components, category, level):
    """
    Compute the combined gov-policy multiplier for a (category, level) pair.

    Each of the 5 gov components may have an entry in GOV_POLICY_MULTIPLIERS.
    Missing entries default to 1.0.  The combined multiplier is the product
    of all 5, clamped to [0.1, 5.0].
    """
    combined = 1.0
    key = (category, level)
    for comp in gov_components:
        comp_mults = GOV_POLICY_MULTIPLIERS.get(comp)
        if comp_mults:
            combined *= comp_mults.get(key, 1.0)
    return max(0.1, min(5.0, combined))


def _scale_effects(effects, multiplier):
    """Return a new dict with all effect values scaled by multiplier."""
    if multiplier == 1.0:
        return effects
    scaled = {}
    for key, value in effects.items():
        if isinstance(value, dict):
            scaled[key] = {k: v * multiplier for k, v in value.items()}
        else:
            scaled[key] = value * multiplier
    return scaled


_NESTED_DICT_KEYS = {"building_efficiency_bonus", "building_efficiency"}


def _merge_into(target, source):
    """
    Merge source effects into target additively.

    Handles ``building_efficiency_bonus`` and ``building_efficiency`` as nested
    dicts of category -> bonus.  All other keys are treated as numeric and summed.
    """
    for key, value in source.items():
        if key in _NESTED_DICT_KEYS:
            if key not in target:
                target[key] = {}
            for cat, bonus in value.items():
                target[key][cat] = target[key].get(cat, 0.0) + bonus
        else:
            target[key] = target.get(key, 0.0) + value


def validate_policy_change(nation, category, new_level):
    """
    Check all disabling sources for a proposed policy change.

    Sources checked (in order):
      1. TRAIT_POLICY_DISABLES — trait-based disabling
      2. GOV_POLICY_DISABLES — government option disabling
      3. POLICY_POLICY_DISABLES — cross-policy disabling
      4. POLICY_REQUIREMENTS — prerequisite requirements (legacy, currently empty)
      5. POLICY_BANS — cross-policy bans (legacy, currently empty)

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

    # Collect nation's trait keys with their strength
    ideology = nation.ideology_traits or {}
    strong_trait = ideology.get("strong")
    weak_traits = ideology.get("weak", [])

    # 1. Check trait-policy disabling
    target = (category, new_level)
    # Check strong trait
    if strong_trait:
        disabled = TRAIT_POLICY_DISABLES.get((strong_trait, "strong"), [])
        if target in disabled:
            errors.append(
                f"Policy {category} level {new_level} is disabled by "
                f"strong trait '{strong_trait}'"
            )
    # Check weak traits
    for wt in weak_traits:
        disabled = TRAIT_POLICY_DISABLES.get((wt, "weak"), [])
        if target in disabled:
            errors.append(
                f"Policy {category} level {new_level} is disabled by "
                f"weak trait '{wt}'"
            )

    # 2. Check gov-policy disabling
    for gov_val in gov_values:
        disabled = GOV_POLICY_DISABLES.get(gov_val, [])
        if target in disabled:
            errors.append(
                f"Policy {category} level {new_level} is disabled by "
                f"government option '{gov_val}'"
            )

    # 3. Check policy-policy disabling
    current_policies = dict(
        NationPolicy.objects.filter(nation=nation)
        .exclude(category=category)
        .values_list("category", "level")
    )

    for target_cat, target_level, when_cat, when_level in POLICY_POLICY_DISABLES:
        if target_cat == category and target_level == new_level:
            current = current_policies.get(when_cat)
            if current is not None and current == when_level:
                when_name = _get_level_name(when_cat, when_level)
                errors.append(
                    f"Policy {category} level {new_level} is disabled when "
                    f"{when_cat} is at '{when_name}'"
                )

    # 4. Check legacy POLICY_REQUIREMENTS
    req = POLICY_REQUIREMENTS.get((category, new_level))
    if req:
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

        nation_traits = set()
        if strong_trait:
            nation_traits.add(strong_trait)
        for w in weak_traits:
            nation_traits.add(w)

        traits_required = req.get("traits_required")
        if traits_required and not nation_traits.intersection(traits_required):
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

        policies_required = req.get("policies_required")
        if policies_required:
            for req_cat, min_level in policies_required:
                current = current_policies.get(req_cat, 0)
                if current < min_level:
                    errors.append(
                        f"Policy {category} level {new_level} requires "
                        f"{req_cat} >= {min_level} (currently {current})"
                    )

    # 5. Check legacy POLICY_BANS
    for (ban_cat, ban_level), banned_list in POLICY_BANS.items():
        if ban_cat == category:
            continue
        current = current_policies.get(ban_cat)
        if current is not None and current == ban_level:
            for banned_cat, banned_level in banned_list:
                if banned_cat == category and banned_level == new_level:
                    errors.append(
                        f"Policy {category} level {new_level} is banned by "
                        f"current policy {ban_cat} level {ban_level}"
                    )

    bans_from_new = POLICY_BANS.get((category, new_level), [])
    for banned_cat, banned_level in bans_from_new:
        if banned_cat == category:
            continue
        current = current_policies.get(banned_cat)
        if current is not None and current == banned_level:
            errors.append(
                f"Policy {category} level {new_level} conflicts with "
                f"current policy {banned_cat} level {banned_level}"
            )

    return errors


def _get_level_name(category, level):
    """Get display name for a policy level, or fall back to the index."""
    cat_def = POLICY_CATEGORIES.get(category, {})
    levels = cat_def.get("levels", [])
    if level < len(levels):
        return levels[level].get("name", str(level))
    return str(level)


def get_policy_building_blocks(nation):
    """
    Return the set of building_types blocked by the nation's current policies.

    Checks:
      1. POLICY_BUILDING_FORBIDDEN — (category, level) → set of building_types
      2. BUILDING_POLICY_REQUIREMENTS — all prereqs must be met (AND logic)
      3. BUILDING_POLICY_BANS — any match blocks
    """
    from .models import NationPolicy

    current_policies = dict(
        NationPolicy.objects.filter(nation=nation)
        .values_list("category", "level")
    )

    blocked = set()

    # Policy-building forbidden: if nation has (cat, level), block those buildings
    for (cat, level), forbidden_buildings in POLICY_BUILDING_FORBIDDEN.items():
        current = current_policies.get(cat)
        if current is not None and current == level:
            blocked.update(forbidden_buildings)

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


def get_security_policy_multiplier(nation):
    """
    Return the aggregate security multiplier from all of a nation's active policies.

    Iterates NationPolicy rows, looks up each (category, level) in
    SECURITY_POLICY_MULTIPLIERS, and returns the product of all matching values.
    Missing entries default to 1.0.
    """
    from .models import NationPolicy

    combined = 1.0
    for policy in NationPolicy.objects.filter(nation=nation):
        level_mult = SECURITY_POLICY_MULTIPLIERS.get(policy.category, {}).get(policy.level, 1.0)
        combined *= level_mult
    return combined


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
