"""
Travel time helpers for the zone adjacency system.

Three entry points:

  get_march_time(p1, p2, national_modifiers)
      Province-to-province march. Uses midpoint distance from center_x/center_y.
      national_modifiers should come from get_national_building_effects(provinces).
      Falls back to DEFAULT_MARCH_TIME if coordinates are null.
      march_speed_bonus is averaged across both provinces' province-scope effects.

  get_embark_time(province, to_zone_type, province_modifiers)
      Province/zone-type cross transition. Uses province.sea_border_distance or
      province.river_border_distance. province_modifiers should come from
      get_province_building_effects(province) so dock's province-scope
      sea_transit_speed / river_transit_speed applies.
      Falls back to DEFAULT_EMBARK_TIME if border distance is null.

  get_zone_travel_time(zone_type, national_modifiers)
      Same-type zone hop (sea->sea, river->river, air->air). Flat base time
      reduced by national speed modifier. Returns 0.0 for free cross-type pairs.

  check_cross_type_requirements(from_type, to_type, from_buildings, to_buildings)
      Returns list of missing building type strings, or [] if requirements met.
"""
import math

from .travel_constants import (
    BASE_ZONE_TRAVEL,
    CROSS_TYPE_PROVINCE_MODIFIER_KEY,
    CROSS_TYPE_REQUIREMENTS,
    DEFAULT_EMBARK_TIME,
    DEFAULT_MARCH_TIME,
    EMBARK_SPEED,
    FREE_CROSS_TYPE_TRANSITIONS,
    MARCH_SPEED,
    MINIMUM_TRAVEL_TURNS,
    ZONE_SPEED_MODIFIER_KEY,
)


def get_march_time(p1, p2, national_modifiers: dict) -> float:
    """
    Province-to-province march time in turns.
    p1, p2: Province model instances.
    national_modifiers: dict from get_national_building_effects().
    Province-scope march_speed_bonus is averaged across both endpoints.
    """
    from economy.building_simulation import get_province_building_effects

    if p1.center_x is None or p2.center_x is None:
        base = DEFAULT_MARCH_TIME
    else:
        dist = math.sqrt((p2.center_x - p1.center_x) ** 2 + (p2.center_y - p1.center_y) ** 2)
        base = dist / MARCH_SPEED

    # Average province-scope march bonus from both endpoints
    e1 = get_province_building_effects(p1).get('march_speed_bonus', 0.0)
    e2 = get_province_building_effects(p2).get('march_speed_bonus', 0.0)
    prov_bonus = (e1 + e2) / 2.0

    # Stack with national march bonus
    nat_bonus = national_modifiers.get('march_speed_bonus', 0.0)
    total_bonus = prov_bonus + nat_bonus

    turns = base / max(1.0, 1.0 + total_bonus)
    return max(MINIMUM_TRAVEL_TURNS, round(turns, 4))


def get_embark_time(province, to_zone_type: str, province_modifiers: dict) -> float:
    """
    Province/zone-type (or zone-type/province) cross-type transition time.
    province: Province model instance (the province end of the transition).
    to_zone_type: 'sea', 'river', or 'air'.
    province_modifiers: dict from get_province_building_effects(province)
      -- dock's sea_transit_speed / river_transit_speed lives here.
    Returns 0.0 for free transitions (sea<->air, river<->air).
    """
    if ('province', to_zone_type) in FREE_CROSS_TYPE_TRANSITIONS:
        return 0.0

    border_dist = None
    if to_zone_type == 'sea':
        border_dist = province.sea_border_distance
    elif to_zone_type == 'river':
        border_dist = province.river_border_distance
    # air: base from DEFAULT_EMBARK_TIME (no distance concept yet)

    if border_dist is None:
        base = DEFAULT_EMBARK_TIME
    else:
        base = border_dist / EMBARK_SPEED

    modifier_key = CROSS_TYPE_PROVINCE_MODIFIER_KEY.get(to_zone_type)
    bonus = province_modifiers.get(modifier_key, 0.0) if modifier_key else 0.0
    turns = base / max(1.0, 1.0 + bonus)
    return max(MINIMUM_TRAVEL_TURNS, round(turns, 4))


def get_zone_travel_time(zone_type: str, national_modifiers: dict) -> float:
    """
    Same-type zone hop (sea->sea, river->river, air->air) time in turns.
    national_modifiers: dict from get_national_building_effects().
    """
    base = BASE_ZONE_TRAVEL.get(zone_type, 1.0)
    key = ZONE_SPEED_MODIFIER_KEY.get(zone_type)
    bonus = national_modifiers.get(key, 0.0) if key else 0.0
    turns = base / max(1.0, 1.0 + bonus)
    return max(MINIMUM_TRAVEL_TURNS, round(turns, 4))


def check_cross_type_requirements(
    from_type: str,
    to_type: str,
    from_buildings: list,
    to_buildings: list,
) -> list:
    """
    Return list of missing requirement descriptions, or [] if all requirements met.
    Each requirement group is satisfied if any building in the group is present.
    """
    reqs = CROSS_TYPE_REQUIREMENTS.get((from_type, to_type), [])
    if not reqs:
        return []
    from_set = set(from_buildings)
    to_set = set(to_buildings)
    missing = []
    for req_group in reqs:
        # req_group is a list of alternatives — any one of them satisfies this requirement
        has_any = any(r in from_set or r in to_set for r in req_group)
        if not has_any:
            missing.append(f"any of: {req_group}")
    return missing
