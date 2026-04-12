"""
Happiness System computation.

Province.local_happiness is recomputed fresh each turn (static recompute,
not incremental drift). It reflects how well the nation's current policies
align with its ideology traits.

Formula:
    raw  = Σ matrix[category][level][trait] × weight  (strong=1.0, weak=0.5)
    happiness = clamp(BASE_HAPPINESS + trait_baselines + raw × SCALE, 0, 100)

Downstream multiplier functions are used by simulation.py and building_simulation.py.
"""

from .happiness_constants import (
    BASE_HAPPINESS,
    HAPPINESS_POLICY_SCALE,
    HAPPINESS_STRONG_WEIGHT,
    HAPPINESS_WEAK_WEIGHT,
    HAPPINESS_WORKER_PRODUCTIVITY_SLOPE,
    HAPPINESS_WORKER_PRODUCTIVITY_BASE,
    HAPPINESS_GROWTH_MULTIPLIER_SLOPE,
    HAPPINESS_GROWTH_MULTIPLIER_BASE,
    HAPPINESS_STABILITY_RECOVERY_MULTIPLIER_SLOPE,
    HAPPINESS_STABILITY_RECOVERY_MULTIPLIER_BASE,
)
from .happiness_policy_data import HAPPINESS_POLICY_MATRIX
from .literacy_constants import LITERACY_HAPPINESS_AMPLIFIER


def compute_province_happiness(province, nation, trait_effects, active_policies, literacy=0.0):
    """
    Compute province happiness (0-100) as a full static recompute.

    Parameters
    ----------
    province : Province
        The province instance (used for future building effect hooks).
    nation : Nation
        The owning nation.
    trait_effects : dict
        Merged trait effects from get_nation_trait_effects(nation).
    active_policies : dict
        {category_key: level_index} for all active NationPolicy rows.
    literacy : float
        Province literacy (0.0–1.0). Higher literacy amplifies the trait-policy
        alignment delta — good alignment becomes better, bad becomes worse.

    Returns
    -------
    float in [0, 100]
    """
    ideology_traits = nation.ideology_traits or {}
    strong_trait = ideology_traits.get("strong")
    weak_traits = ideology_traits.get("weak", [])

    # --- Trait-policy matrix contribution ---
    raw = 0.0
    for category_key, level_index in active_policies.items():
        level_scores = HAPPINESS_POLICY_MATRIX.get(category_key, {}).get(level_index, {})
        if not level_scores:
            continue
        if strong_trait:
            raw += level_scores.get(strong_trait, 0) * HAPPINESS_STRONG_WEIGHT
        for weak_trait in weak_traits:
            raw += level_scores.get(weak_trait, 0) * HAPPINESS_WEAK_WEIGHT

    # --- Trait baseline bonuses (flat additions to happiness, not scaled) ---
    trait_baselines = (
        trait_effects.get("happiness_baseline_bonus", 0.0)
        + trait_effects.get("happiness_baseline_penalty", 0.0)
    )

    # --- Province building bonus (stub — no buildings declare this yet) ---
    # Future: bldg_effects.get("happiness_generation_bonus", 0.0)

    # --- Literacy amplification ---
    # Higher literacy amplifies the alignment delta from BASE_HAPPINESS.
    # At 0% literacy: amplifier = 1.0 (no change).
    # At 100% literacy: amplifier = 1.5 (deltas 50% stronger).
    raw_delta = trait_baselines + raw * HAPPINESS_POLICY_SCALE
    amplifier = 1.0 + literacy * LITERACY_HAPPINESS_AMPLIFIER
    happiness = BASE_HAPPINESS + raw_delta * amplifier
    return max(0.0, min(100.0, happiness))


# ---------------------------------------------------------------------------
# Downstream multiplier functions
# ---------------------------------------------------------------------------

def get_happiness_worker_productivity(happiness):
    """
    Worker productivity multiplier from province happiness.
    Linear: 0.8× at happiness 0, 1.0× at 50, 1.2× at 100.
    Applied as a multiplier on building output.
    """
    return HAPPINESS_WORKER_PRODUCTIVITY_BASE + happiness * HAPPINESS_WORKER_PRODUCTIVITY_SLOPE


def get_happiness_growth_multiplier(happiness):
    """
    Province growth rate multiplier from happiness.
    Linear: 0.9× at happiness 0, 1.0× at 50, 1.1× at 100.
    Multiplied into the growth rate after all additive bonuses are applied.
    """
    return HAPPINESS_GROWTH_MULTIPLIER_BASE + happiness * HAPPINESS_GROWTH_MULTIPLIER_SLOPE


def get_happiness_stability_recovery_multiplier(happiness):
    """
    Stability recovery rate multiplier from province happiness.
    Linear: 0.9× at happiness 0, 1.0× at 50, 1.1× at 100.
    Applied to the effective recovery after all additive bonuses.
    """
    return (
        HAPPINESS_STABILITY_RECOVERY_MULTIPLIER_BASE
        + happiness * HAPPINESS_STABILITY_RECOVERY_MULTIPLIER_SLOPE
    )
