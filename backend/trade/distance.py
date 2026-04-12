"""
Effective distance calculations for trade routes.

The effective distance between two adjacent provinces accounts for:
  1. Euclidean distance between province centres (or a fallback)
  2. Relief multiplier (terrain roughness)
  3. Vegetation multiplier (density of ground cover)
  4. Temperature multiplier (climate extremes)
  5. March speed bonus from buildings (province-scope averaged, national stacked)

Formula:
  raw_dist     = euclidean(p1.center, p2.center)  — or DEFAULT_LAND_HOP if null
  env_mult     = avg(relief_mult) × avg(veg_mult) × avg(temp_mult)
  speed_factor = 1 + avg(prov_march_bonus) + national_march_bonus
  eff_dist     = raw_dist × env_mult / max(1.0, speed_factor)

The multipliers are averaged across both endpoints because a trade route
crosses from one province into another — both terrains contribute friction.
"""
import math

from .constants import (
    RELIEF_TRADE_MULT,
    VEGETATION_TRADE_MULT,
    TEMPERATURE_TRADE_MULT,
)

# Fallback distance when province coordinates are not yet set (pre-map).
DEFAULT_LAND_HOP = 100.0


def _euclidean(p1, p2) -> float:
    """Euclidean distance between two province centres, or fallback."""
    if p1.center_x is None or p2.center_x is None:
        return DEFAULT_LAND_HOP
    return math.sqrt(
        (p2.center_x - p1.center_x) ** 2
        + (p2.center_y - p1.center_y) ** 2
    )


def _env_mult(p1, p2) -> float:
    """Combined environment multiplier averaged across both provinces."""
    r1 = RELIEF_TRADE_MULT.get(p1.relief, 1.0)
    r2 = RELIEF_TRADE_MULT.get(p2.relief, 1.0)

    v1 = VEGETATION_TRADE_MULT.get(p1.vegetation_level, 1.0)
    v2 = VEGETATION_TRADE_MULT.get(p2.vegetation_level, 1.0)

    t1 = TEMPERATURE_TRADE_MULT.get(p1.temperature_band, 1.0)
    t2 = TEMPERATURE_TRADE_MULT.get(p2.temperature_band, 1.0)

    return ((r1 + r2) / 2.0) * ((v1 + v2) / 2.0) * ((t1 + t2) / 2.0)


def effective_land_distance(
    p1,
    p2,
    p1_building_effects: dict | None = None,
    p2_building_effects: dict | None = None,
    national_modifiers: dict | None = None,
) -> float:
    """Compute the effective land distance between two adjacent provinces.

    Parameters
    ----------
    p1, p2 : Province model instances (need center_x/y, relief,
             vegetation_level, temperature_band).
    p1_building_effects, p2_building_effects :
        Province-scope building effects dicts (from
        get_province_building_effects). Pass None to ignore.
    national_modifiers :
        National-scope building effects dict (from
        get_national_building_effects). Pass None to ignore.

    Returns
    -------
    float — effective distance in map-unit equivalents (always > 0).
    """
    raw = _euclidean(p1, p2)
    env = _env_mult(p1, p2)

    # Province-scope march speed bonus averaged across endpoints
    e1 = (p1_building_effects or {}).get("march_speed_bonus", 0.0)
    e2 = (p2_building_effects or {}).get("march_speed_bonus", 0.0)
    prov_bonus = (e1 + e2) / 2.0

    nat_bonus = (national_modifiers or {}).get("march_speed_bonus", 0.0)
    speed_factor = max(1.0, 1.0 + prov_bonus + nat_bonus)

    return max(0.01, raw * env / speed_factor)


def effective_land_distance_simple(p1, p2) -> float:
    """Simplified version without building modifiers — for quick estimates."""
    raw = _euclidean(p1, p2)
    env = _env_mult(p1, p2)
    return max(0.01, raw * env)
