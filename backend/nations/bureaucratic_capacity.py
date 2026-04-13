"""
Bureaucratic Capacity System — core logic.

Computes supply (from buildings, policies, government, traits), demand
(from high-tier policy costs), validates policy changes against capacity,
and applies deficit penalties during turn simulation.

Supply = building_base × (1 + policy_bonus) × gov_multiplier × trait_multiplier
Demand = Σ per-policy costs at consuming tiers
"""

from .bureaucratic_constants import (
    BUREAUCRATIC_BASE_COST,
    BUREAUCRATIC_COST_MULTIPLIER,
    BUREAUCRATIC_CATEGORY_TYPE,
    CATEGORY_COST_MULTIPLIERS,
    ALWAYS_EXEMPT_CATEGORIES,
    ECOLOGIST_EXEMPT_CATEGORIES,
    GOV_BUREAUCRATIC_CAPACITY_MULTIPLIER,
    GOV_MULTIPLIER_MIN,
    GOV_MULTIPLIER_MAX,
    TRAIT_BUREAUCRATIC_CAPACITY_MULTIPLIER,
    TRAIT_TREATY_COST_REDUCTION,
    TREATY_BUREAUCRATIC_BASE_COST,
    DEFICIT_STABILITY_PENALTY_PER_PCT,
    DEFICIT_STABILITY_PENALTY_CAP,
    get_consuming_tier_count,
)
from .policy_effects_data import POLICY_CATEGORIES


# ---------------------------------------------------------------------------
# Tier helpers
# ---------------------------------------------------------------------------

def get_consuming_tiers(total_tiers):
    """
    Return the 0-indexed tier indices that consume bureaucratic capacity.

    The top N tiers consume, where N depends on how many tiers the category has:
      ≤3 tiers  → top 1
      4–5 tiers → top 2
      6–7 tiers → top 3
      8+ tiers  → top 4

    Returns a list sorted ascending (lowest consuming tier first).
    """
    n = get_consuming_tier_count(total_tiers)
    return list(range(total_tiers - n, total_tiers))


def get_tier_cost(tier_index, consuming_tiers):
    """
    Return the bureaucratic cost for a tier given the consuming tier list.

    The lowest consuming tier costs BUREAUCRATIC_BASE_COST.
    Each successive tier doubles: base, base×2, base×4, base×8.

    Parameters
    ----------
    tier_index : int
        0-indexed tier of the policy.
    consuming_tiers : list[int]
        Sorted ascending list of consuming tier indices.

    Returns
    -------
    float
        Cost for this tier, or 0.0 if not a consuming tier.
    """
    if tier_index not in consuming_tiers:
        return 0.0
    position = consuming_tiers.index(tier_index)
    return BUREAUCRATIC_BASE_COST * (BUREAUCRATIC_COST_MULTIPLIER ** position)


# ---------------------------------------------------------------------------
# Supply
# ---------------------------------------------------------------------------

def compute_bureaucratic_supply(nation, provinces=None):
    """
    Compute total bureaucratic capacity for a nation.

    Supply = building_base × (1 + policy_bonus) × gov_multiplier × trait_multiplier

    Parameters
    ----------
    nation : Nation model instance
    provinces : list[Province] or None
        Pre-fetched province queryset. If None, fetched from DB.

    Returns
    -------
    dict with keys:
        building_base   : float — raw sum of bureaucratic_capacity from buildings
        policy_bonus    : float — summed policy effects (fractional, e.g. 0.06)
        gov_multiplier  : float — product of 5 axis multipliers (clamped)
        trait_multiplier : float — product of applicable trait multipliers
        total           : float — final capacity
    """
    # Lazy imports to avoid circular dependency with policy_effects.py
    from economy.building_simulation import get_national_building_effects
    from .policy_effects import get_nation_policy_effects
    from .helpers import get_nation_trait_effects

    if provinces is None:
        provinces = list(nation.provinces.all())

    # 1. Building base — already summed by get_national_building_effects
    national_bldg = get_national_building_effects(provinces)
    building_base = national_bldg.get("bureaucratic_capacity", 0.0)

    # 2. Policy bonus — the bureaucratic_capacity key from merged policy effects
    #    Treated as a multiplicative fraction on the building base (e.g. 0.06 → ×1.06).
    policy_effects = get_nation_policy_effects(nation)
    policy_bonus = policy_effects.get("bureaucratic_capacity", 0.0)

    # 3. Government multiplier — product of all 5 axis values
    gov_values = [
        nation.gov_direction,
        nation.gov_economic_category,
        nation.gov_structure,
        nation.gov_power_origin,
        nation.gov_power_type,
    ]
    gov_multiplier = 1.0
    for val in gov_values:
        gov_multiplier *= GOV_BUREAUCRATIC_CAPACITY_MULTIPLIER.get(val, 1.0)
    gov_multiplier = max(GOV_MULTIPLIER_MIN, min(GOV_MULTIPLIER_MAX, gov_multiplier))

    # 4. Trait multiplier
    ideology_traits = nation.ideology_traits or {}
    strong_trait = ideology_traits.get("strong")
    weak_traits = ideology_traits.get("weak", [])

    trait_multiplier = 1.0
    if strong_trait and strong_trait in TRAIT_BUREAUCRATIC_CAPACITY_MULTIPLIER:
        trait_multiplier *= TRAIT_BUREAUCRATIC_CAPACITY_MULTIPLIER[strong_trait]["strong"]
    for wt in weak_traits:
        if wt in TRAIT_BUREAUCRATIC_CAPACITY_MULTIPLIER:
            trait_multiplier *= TRAIT_BUREAUCRATIC_CAPACITY_MULTIPLIER[wt]["weak"]

    total = building_base * (1.0 + policy_bonus) * gov_multiplier * trait_multiplier

    return {
        "building_base": round(building_base, 4),
        "policy_bonus": round(policy_bonus, 4),
        "gov_multiplier": round(gov_multiplier, 4),
        "trait_multiplier": round(trait_multiplier, 4),
        "total": round(total, 4),
    }


# ---------------------------------------------------------------------------
# Demand
# ---------------------------------------------------------------------------

def _get_nation_trait_keys(nation):
    """Return a set of all trait keys the nation has (strong + weak)."""
    ideology = nation.ideology_traits or {}
    traits = set()
    strong = ideology.get("strong")
    if strong:
        traits.add(strong)
    for w in ideology.get("weak", []):
        traits.add(w)
    return traits


def _has_ecologist(nation_traits):
    """Return True if ecologist is among the nation's traits."""
    return "ecologist" in nation_traits


def compute_policy_bureaucratic_cost(category, level, total_tiers, nation_traits=None):
    """
    Compute bureaucratic cost for a single policy at a given level.

    Returns 0 if:
      - The category is in ALWAYS_EXEMPT_CATEGORIES
      - The category is in ECOLOGIST_EXEMPT_CATEGORIES and nation has ecologist
      - The level is not a consuming tier

    Parameters
    ----------
    category : str — policy category key
    level : int — 0-indexed tier
    total_tiers : int — total number of tiers in this category
    nation_traits : set[str] or None — trait keys the nation has

    Returns
    -------
    float — bureaucratic cost for this policy setting
    """
    if nation_traits is None:
        nation_traits = set()

    # Always-exempt categories
    if category in ALWAYS_EXEMPT_CATEGORIES:
        return 0.0

    # Ecologist exemption at consuming tiers
    if category in ECOLOGIST_EXEMPT_CATEGORIES and _has_ecologist(nation_traits):
        return 0.0

    # Determine consuming tiers
    consuming = get_consuming_tiers(total_tiers)
    if level not in consuming:
        return 0.0

    # Positional cost (exponential ramp)
    base_cost = get_tier_cost(level, consuming)

    # Category multiplier
    cat_type = BUREAUCRATIC_CATEGORY_TYPE.get(category, "neutral")
    cat_mult = CATEGORY_COST_MULTIPLIERS.get(cat_type, 1.0)

    return round(base_cost * cat_mult, 4)


def compute_total_bureaucratic_demand(nation, proposed_change=None):
    """
    Sum bureaucratic costs across all active policies for a nation.

    Parameters
    ----------
    nation : Nation model instance
    proposed_change : tuple (category, new_level) or None
        If provided, substitutes this level for the given category.

    Returns
    -------
    dict with keys:
        per_policy : dict[str, float] — category → cost (only non-zero entries)
        total      : float
    """
    from .models import NationPolicy

    nation_traits = _get_nation_trait_keys(nation)

    # Build current policy levels
    current_levels = {}
    for policy in NationPolicy.objects.filter(nation=nation):
        current_levels[policy.category] = policy.level

    # Apply proposed change
    if proposed_change:
        current_levels[proposed_change[0]] = proposed_change[1]

    per_policy = {}
    total = 0.0

    for category, level in current_levels.items():
        cat_def = POLICY_CATEGORIES.get(category)
        if not cat_def:
            continue
        total_tiers = len(cat_def["levels"])
        cost = compute_policy_bureaucratic_cost(category, level, total_tiers, nation_traits)
        if cost > 0:
            per_policy[category] = cost
            total += cost

    return {
        "per_policy": per_policy,
        "total": round(total, 4),
    }


# ---------------------------------------------------------------------------
# Validation (policy change gate)
# ---------------------------------------------------------------------------

def validate_bureaucratic_capacity(nation, category, new_level):
    """
    Check if a proposed policy change would exceed bureaucratic capacity.

    Returns a list of error strings. Empty list means the change is valid.
    """
    cat_def = POLICY_CATEGORIES.get(category)
    if not cat_def:
        return []

    total_tiers = len(cat_def["levels"])
    nation_traits = _get_nation_trait_keys(nation)

    # Quick exit: if the proposed level doesn't consume capacity, always OK
    proposed_cost = compute_policy_bureaucratic_cost(
        category, new_level, total_tiers, nation_traits
    )
    if proposed_cost == 0:
        return []

    supply = compute_bureaucratic_supply(nation)
    demand = compute_total_bureaucratic_demand(nation, proposed_change=(category, new_level))

    if demand["total"] > supply["total"]:
        level_name = cat_def["levels"][new_level]["name"] if new_level < total_tiers else str(new_level)
        return [
            f"Insufficient bureaucratic capacity for {category} at "
            f"'{level_name}': requires {demand['total']:.1f} total "
            f"(this policy costs {proposed_cost:.1f}), "
            f"but nation only has {supply['total']:.1f} capacity"
        ]

    return []


# ---------------------------------------------------------------------------
# Deficit penalties (turn simulation)
# ---------------------------------------------------------------------------

def compute_bureaucratic_deficit_penalties(supply_total, demand_total, per_policy_costs):
    """
    Compute penalties when bureaucratic demand exceeds supply.

    The most expensive policies lose benefits first (waterfall allocation:
    cheapest policies are funded first from available capacity).

    Parameters
    ----------
    supply_total : float — total bureaucratic capacity
    demand_total : float — total bureaucratic demand
    per_policy_costs : dict[str, float] — category → cost (non-zero only)

    Returns
    -------
    dict with keys:
        deficit_ratio             : float — (demand - supply) / demand, 0–1
        stability_penalty         : float — monthly stability hit
        policy_benefit_reductions : dict[str, float] — category → funded fraction (0.0–1.0)
        global_benefit_factor     : float — weighted-average reduction factor for merged effects
    """
    if demand_total <= 0 or supply_total >= demand_total:
        return {
            "deficit_ratio": 0.0,
            "stability_penalty": 0.0,
            "policy_benefit_reductions": {},
            "global_benefit_factor": 1.0,
        }

    deficit_ratio = (demand_total - supply_total) / demand_total

    # Stability penalty
    stability_penalty = min(
        deficit_ratio * 100.0 * DEFICIT_STABILITY_PENALTY_PER_PCT,
        DEFICIT_STABILITY_PENALTY_CAP,
    )

    # Waterfall benefit reduction: fund cheapest policies first.
    # Sort ascending by cost so cheapest get funded before expensive ones.
    sorted_policies = sorted(per_policy_costs.items(), key=lambda x: x[1])
    remaining_capacity = supply_total
    policy_factors = {}

    for category, cost in sorted_policies:
        if cost <= 0:
            policy_factors[category] = 1.0
            continue
        if remaining_capacity >= cost:
            policy_factors[category] = 1.0
            remaining_capacity -= cost
        elif remaining_capacity > 0:
            policy_factors[category] = remaining_capacity / cost
            remaining_capacity = 0.0
        else:
            policy_factors[category] = 0.0

    # Weighted-average global factor for reducing merged policy effects.
    # Only policies with non-zero cost participate in the weighting.
    total_weighted = 0.0
    total_cost = 0.0
    for category, cost in per_policy_costs.items():
        if cost > 0:
            total_weighted += cost * policy_factors.get(category, 0.0)
            total_cost += cost

    global_factor = total_weighted / total_cost if total_cost > 0 else 1.0

    return {
        "deficit_ratio": round(deficit_ratio, 4),
        "stability_penalty": round(stability_penalty, 4),
        "policy_benefit_reductions": policy_factors,
        "global_benefit_factor": round(global_factor, 4),
    }


def apply_deficit_to_policy_effects(policy_effects, global_benefit_factor):
    """
    Reduce positive policy effects by the global benefit factor.

    Positive (beneficial) effect values are scaled down. Negative
    (penalty/drawback) values pass through at full force.

    Parameters
    ----------
    policy_effects : dict — merged effects from get_nation_policy_effects()
    global_benefit_factor : float — 0.0 to 1.0

    Returns
    -------
    dict — new dict with positive values scaled, negative values unchanged
    """
    if global_benefit_factor >= 1.0:
        return policy_effects

    adjusted = {}
    for key, value in policy_effects.items():
        if isinstance(value, dict):
            # Nested dict (e.g. building_efficiency_bonus): scale positive sub-values
            adjusted[key] = {
                k: v * global_benefit_factor if v > 0 else v
                for k, v in value.items()
            }
        elif isinstance(value, (int, float)):
            adjusted[key] = value * global_benefit_factor if value > 0 else value
        else:
            adjusted[key] = value

    return adjusted


# ---------------------------------------------------------------------------
# Treaty stub (future diplomacy system)
# ---------------------------------------------------------------------------

def compute_treaty_bureaucratic_cost(nation_traits=None):
    """
    Compute bureaucratic cost to maintain a treaty.

    Stub for the future diplomacy system. Returns the base cost, reduced
    by the Internationalist trait if present.

    Parameters
    ----------
    nation_traits : set[str] or None — trait keys the nation has

    Returns
    -------
    float — bureaucratic cost per treaty
    """
    if nation_traits is None:
        nation_traits = set()

    cost = TREATY_BUREAUCRATIC_BASE_COST

    # Check for Internationalist reduction.
    # We don't know strong vs weak from just the trait set, so we check
    # both and apply the larger reduction if strong is present.
    # This is a simplification — the calling code should pass strength info
    # when the diplomacy system is actually built.
    if "internationalist" in nation_traits:
        # Default to weak reduction; strong requires caller context
        reduction = TRAIT_TREATY_COST_REDUCTION["internationalist"]["weak"]
        cost *= (1.0 - reduction)

    return round(cost, 4)
