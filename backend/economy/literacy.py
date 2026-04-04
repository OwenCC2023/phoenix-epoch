"""
Literacy system computation.

Province.literacy (0.0–1.0) is updated each turn using an S-curve growth
formula driven by buildings, security, wealth, and policy state.

National literacy (mean of province literacies) multiplies research production
each turn and amplifies happiness deltas.
"""

from .literacy_constants import (
    BASE_LITERACY_GROWTH,
    WEALTH_LITERACY_SCALE,
    WEALTH_LITERACY_CAP,
    POP_GROWTH_DILUTION_THRESHOLD,
    POP_GROWTH_DILUTION_FACTOR,
    CHILD_LABOR_LITERACY_PENALTY,
    SLAVERY_LITERACY_GROWTH_PENALTY,
    SLAVERY_LITERACY_CAP,
    LITERACY_HAPPINESS_AMPLIFIER,
)
from .research_constants import (
    BASE_MAX_BUILDING_LEVEL,
    RESEARCH_LITERACY_BASE,
    RESEARCH_LITERACY_SCALE,
    RESEARCH_UNLOCK_COSTS,
)
from .security import get_security_literacy_multiplier


def compute_literacy_growth(
    province,
    bldg_effects: dict,
    security: float,
    wealth_per_cap: float,
    pop_growth_rate: float,
    active_policies: dict,
    trait_effects: dict,
) -> float:
    """
    Compute the new literacy value for a province after one turn of growth.

    Parameters
    ----------
    province : Province
        Province instance with current .literacy value.
    bldg_effects : dict
        Province building effects from get_province_building_effects(province).
        Uses "literacy_bonus" key.
    security : float
        Province local security (0-100), already computed this turn.
    wealth_per_cap : float
        Wealth produced this turn divided by province population.
    pop_growth_rate : float
        Province population growth rate from last turn (0.0 if first turn).
    active_policies : dict
        {category: level_index} for all active NationPolicy rows.
    trait_effects : dict
        Merged trait effects from get_nation_trait_effects(nation).
        Uses "literacy_bonus" key.

    Returns
    -------
    float in [0.0, 1.0]
        Updated literacy for this province.
    """
    literacy = province.literacy

    # --- S-curve base growth ---
    # Formula: BASE * lit * (1-lit) * 4
    # Normalised so peak growth (at 50%) equals BASE_LITERACY_GROWTH.
    base_growth = BASE_LITERACY_GROWTH * literacy * (1.0 - literacy) * 4.0

    # --- Building literacy bonus (additive multiplier) ---
    # Collect literacy_bonus from buildings, traits, and policies (already
    # merged into trait_effects and bldg_effects by the simulation).
    literacy_bonus = (
        bldg_effects.get("literacy_bonus", 0.0)
        + trait_effects.get("literacy_bonus", 0.0)
    )
    growth_after_buildings = base_growth * (1.0 + literacy_bonus)

    # --- Security multiplier ---
    security_mult = get_security_literacy_multiplier(security)
    growth_after_security = growth_after_buildings * security_mult

    # --- Wealth multiplier ---
    wealth_bonus = min(wealth_per_cap / WEALTH_LITERACY_SCALE, WEALTH_LITERACY_CAP)
    growth_after_wealth = growth_after_security * (1.0 + wealth_bonus)

    # --- Population growth dilution ---
    # Rapid pop growth dilutes literacy % (more illiterates added than literates).
    if pop_growth_rate > POP_GROWTH_DILUTION_THRESHOLD:
        excess = pop_growth_rate - POP_GROWTH_DILUTION_THRESHOLD
        dilution = excess * 10.0 * POP_GROWTH_DILUTION_FACTOR
        growth_after_dilution = growth_after_wealth * max(0.0, 1.0 - dilution)
    else:
        growth_after_dilution = growth_after_wealth

    # --- Policy penalties ---
    child_labor_level = active_policies.get("child_labor", 0)
    slavery_level = active_policies.get("slavery", 0)

    child_penalty = CHILD_LABOR_LITERACY_PENALTY.get(child_labor_level, 0.0)
    slavery_growth_penalty = SLAVERY_LITERACY_GROWTH_PENALTY.get(slavery_level, 0.0)

    final_growth = growth_after_dilution * (1.0 + child_penalty) * (1.0 + slavery_growth_penalty)

    # Growth never goes negative (policies slow, never reverse literacy).
    final_growth = max(0.0, final_growth)

    # --- Apply growth ---
    new_literacy = literacy + final_growth

    # --- Slavery literacy cap ---
    slavery_cap = SLAVERY_LITERACY_CAP.get(slavery_level, 1.0)
    new_literacy = min(new_literacy, slavery_cap)

    return max(0.0, min(1.0, new_literacy))


def get_national_literacy(provinces) -> float:
    """
    Return the mean literacy across all provinces.

    Parameters
    ----------
    provinces : list of Province
        Province instances with up-to-date .literacy values.

    Returns
    -------
    float in [0.0, 1.0]
    """
    if not provinces:
        return 0.0
    return sum(p.literacy for p in provinces) / len(provinces)


def get_literacy_research_multiplier(national_literacy: float) -> float:
    """
    Return the multiplier applied to national research production based on
    the national average literacy.

    At 20% literacy: 0.5× (early game research is halved)
    At 50% literacy: 0.8×
    At 80% literacy: 1.1×
    At 100% literacy: 1.3× (bonus for fully literate nations)
    """
    return RESEARCH_LITERACY_BASE + national_literacy * RESEARCH_LITERACY_SCALE


def get_literacy_happiness_amplifier(literacy: float) -> float:
    """
    Return the multiplier on happiness deltas from the trait-policy alignment score.

    At 0%:   1.0× (no amplification)
    At 50%:  1.25×
    At 100%: 1.5×

    High literacy makes good alignment feel even better and bad alignment worse.
    """
    return 1.0 + literacy * LITERACY_HAPPINESS_AMPLIFIER


def get_max_building_level(nation, sector: str) -> int:
    """
    Return the maximum building level a nation may construct in a given sector.

    Parameters
    ----------
    nation : Nation
        The owning nation.
    sector : str
        Building category key (e.g. "heavy_manufacturing").

    Returns
    -------
    int
        Maximum constructible level (2 base, +2 per unlock tier).
    """
    if sector not in RESEARCH_UNLOCK_COSTS:
        # Sector has no unlock defined — allow base max only.
        return BASE_MAX_BUILDING_LEVEL

    from .models import ResearchUnlock
    try:
        unlock = ResearchUnlock.objects.get(nation=nation, sector=sector)
        return BASE_MAX_BUILDING_LEVEL + unlock.tier * 2
    except ResearchUnlock.DoesNotExist:
        return BASE_MAX_BUILDING_LEVEL
