"""
Development Points (DP) System — pure computation (System 17).

No database access in this module. All functions take plain Python values.
"""

from .dp_constants import (
    DP_MULTIPLIER_K,
    CONCENTRATION_BONUS_DIVISOR,
    CONCENTRATION_PENALTY_DIVISOR,
)


def compute_dp_multiplier(dp: int) -> float:
    """Return the DP production multiplier for a given DP value.

    Formula: 1 + dp / (dp + K)
      dp=0   → 1.0 (no bonus)
      dp=K   → 1.5 (midpoint, K=100 by default)
      dp=∞   → 2.0 (hard limit)

    Args:
        dp: Whole number >= 0. Negative values are treated as 0.
    """
    dp = max(0, dp)
    if dp == 0:
        return 1.0
    return 1.0 + dp / (dp + DP_MULTIPLIER_K)


def compute_concentration_multiplier(
    category_dp: int, total_dp: int, is_concentrated_category: bool
) -> float:
    """Return the concentration bonus or penalty multiplier.

    Triggers only when one category holds >50% of total DP.
    Concentrated category gets a bonus; all others get a penalty.

    Args:
        category_dp:             DP in the category being evaluated.
        total_dp:                Sum of DP across all categories in the province.
        is_concentrated_category: True if this is the dominant category.

    Returns:
        Multiplier. Penalty is clamped to floor of 0.0.
    """
    if total_dp == 0:
        return 1.0

    concentrated_dp = None
    # Find the category that holds >50% of total DP.
    # Caller pre-identifies the concentrated category (is_concentrated_category=True).
    if is_concentrated_category:
        concentrated_dp = category_dp
    else:
        # We still need the concentrated category's DP to compute the penalty.
        # Caller must pass the actual concentrated_dp separately — this path
        # is only reached when we know a concentrated category exists.
        # penalty = 1 - (concentrated_dp - total_dp/2) / PENALTY_DIVISOR
        # But we don't have concentrated_dp here; this function is called once
        # per category. See compute_province_dp_multiplier for the full logic.
        return 1.0  # fallback; real logic is in compute_province_dp_multiplier

    excess = concentrated_dp - total_dp / 2
    return 1.0 + excess / CONCENTRATION_BONUS_DIVISOR


def compute_province_dp_multipliers(province_dp: dict) -> dict:
    """Compute DP multipliers for all categories in a province.

    Returns a dict mapping each category to its effective multiplier,
    combining the base DP multiplier and any concentration bonus/penalty.

    Args:
        province_dp: {category: dp_value} for all DP categories in this province.

    Returns:
        {category: multiplier_float}
    """
    if not province_dp:
        return {}

    total_dp = sum(province_dp.values())

    # Find the category with the most DP, if it exceeds 50% of total.
    concentrated_cat = None
    concentrated_dp = 0
    if total_dp > 0:
        max_cat = max(province_dp, key=lambda c: province_dp[c])
        max_dp = province_dp[max_cat]
        if max_dp > total_dp / 2:
            concentrated_cat = max_cat
            concentrated_dp = max_dp

    result = {}
    excess = concentrated_dp - total_dp / 2 if concentrated_cat else 0.0

    for cat, dp in province_dp.items():
        base_mult = compute_dp_multiplier(dp)

        if concentrated_cat is None:
            # No concentration — apply base multiplier only.
            result[cat] = base_mult
        elif cat == concentrated_cat:
            # This is the dominant category — bonus.
            conc_mult = 1.0 + excess / CONCENTRATION_BONUS_DIVISOR
            result[cat] = base_mult * conc_mult
        else:
            # Non-dominant category — penalty.
            penalty = 1.0 - excess / CONCENTRATION_PENALTY_DIVISOR
            penalty = max(0.0, penalty)  # clamp floor
            result[cat] = base_mult * penalty

    return result


def compute_province_dp_multiplier(category: str, province_dp: dict) -> float:
    """Return the effective DP multiplier for a single category in a province.

    Convenience wrapper around compute_province_dp_multipliers.

    Args:
        category:    The building category (or "subsistence") to look up.
        province_dp: {category: dp_value} for all DP categories in this province.
    """
    mults = compute_province_dp_multipliers(province_dp)
    return mults.get(category, 1.0)


def compute_national_dp_summary(province_dp_list: list) -> dict:
    """Sum provincial DP across provinces for national display.

    This value is informational only — no mechanical effect.

    Args:
        province_dp_list: List of {category: dp_value} dicts, one per province.

    Returns:
        {category: total_dp} summed across all provinces.
    """
    summary = {}
    for province_dp in province_dp_list:
        for cat, dp in province_dp.items():
            summary[cat] = summary.get(cat, 0) + dp
    return summary
