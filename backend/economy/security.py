import math

from .security_constants import (
    BASE_SECURITY,
    SECURITY_STABILITY_FLOOR,
    SECURITY_STABILITY_CAP,
    SECURITY_LITERACY_FLOOR,
    SECURITY_LITERACY_CAP,
    SECURITY_GROWTH_THRESHOLD,
    SECURITY_GROWTH_MAX_BONUS,
    SECURITY_FOOD_DEFICIT_PENALTY,
    SECURITY_FOOD_SEVERE_PENALTY,
    SECURITY_IMMIGRATION_PENALTY_RATE,
    SECURITY_IMMIGRATION_PENALTY_CAP,
)


def get_security_stability_multiplier(security: float) -> float:
    """
    Maps province security (0-100) to a stability multiplier (0.5-1.5).
    Linear from 0-50, logarithmic from 50-100 (diminishing returns at high security).

    Calibration points:
      security  0 → 0.50
      security 30 → 0.90  (base)
      security 50 → 1.167
      security 100→ 1.50
    """
    security = max(0.0, min(100.0, security))
    if security <= 50:
        return SECURITY_STABILITY_FLOOR + security / 75.0
    f50 = SECURITY_STABILITY_FLOOR + 50.0 / 75.0  # ≈ 1.1667
    return f50 + (SECURITY_STABILITY_CAP - f50) * math.log2(1.0 + (security - 50.0) / 50.0)


def get_security_literacy_multiplier(security: float) -> float:
    """
    Maps province security (0-100) to a literacy multiplier (0.7-1.2).
    Linear from 0-50, logarithmic from 50-100.

    Calibration points:
      security  0 → 0.70
      security 30 → 0.90  (base)
      security 50 → 1.033
      security 100→ 1.20
    """
    security = max(0.0, min(100.0, security))
    if security <= 50:
        return SECURITY_LITERACY_FLOOR + security / 150.0
    f50 = SECURITY_LITERACY_FLOOR + 50.0 / 150.0  # ≈ 1.0333
    return f50 + (SECURITY_LITERACY_CAP - f50) * math.log2(1.0 + (security - 50.0) / 50.0)


def get_security_growth_bonus(security: float) -> float:
    """
    Small per-month growth bonus when security exceeds 50.
    Linear from 0 at security=50 to SECURITY_GROWTH_MAX_BONUS at security=100.
    """
    if security <= SECURITY_GROWTH_THRESHOLD:
        return 0.0
    return SECURITY_GROWTH_MAX_BONUS * (security - SECURITY_GROWTH_THRESHOLD) / (
        100.0 - SECURITY_GROWTH_THRESHOLD
    )


def compute_province_security(
    bldg_effects: dict,
    policy_security_mult: float,
    trait_security_mult: float,
    food_ratio: float,
    net_immigration_pct: float,
    has_internationalist: bool,
) -> float:
    """
    Compute the security value for a province for this turn.

    Args:
        bldg_effects: Province-scope building effects dict (from get_province_building_effects).
        policy_security_mult: Product of all active policy security_multiplier values.
        trait_security_mult: Nation's security multiplier from honorable/devious trait (or 1.0).
        food_ratio: Province effective food ratio (local + national supplement / consumption).
                    Values < 1.0 indicate a deficit; < 0.5 is severe.
        net_immigration_pct: Fraction of province population that immigrated this turn.
                             Positive = net inflow. 0.01 = 1% of population arrived.
        has_internationalist: True if nation has internationalist trait (strong or weak);
                              waives the immigration security penalty.

    Returns:
        Security value clamped to [0, 100].
    """
    raw = BASE_SECURITY + bldg_effects.get("security", 0.0)
    modified = raw * policy_security_mult * trait_security_mult

    # Food penalties (applied after multiplicative modifiers)
    if food_ratio < 0.5:
        modified += SECURITY_FOOD_SEVERE_PENALTY
    elif food_ratio < 1.0:
        modified += SECURITY_FOOD_DEFICIT_PENALTY

    # Immigration penalty (waived for Internationalist nations)
    if not has_internationalist and net_immigration_pct > 0.0:
        penalty = net_immigration_pct * 100.0 * SECURITY_IMMIGRATION_PENALTY_RATE
        modified += max(SECURITY_IMMIGRATION_PENALTY_CAP, penalty)

    return max(0.0, min(100.0, modified))
