"""
Development Points (DP) System — game-start initialization (System 17).

Called once from initialize_whitespace() when a game transitions to ACTIVE.
Creates ProvinceDevelopmentPoints rows for every province and NationDPPool /
NationMilitaryDP rows for every nation in the game.
"""

import random

from provinces.constants import TERRAIN_TYPES
from .dp_constants import (
    DP_BUILDING_CATEGORIES,
    BUILDING_CATEGORY_TO_SECTOR,
    MILITARY_DP_CATEGORIES,
    DP_INIT_TOTAL_MIN,
    DP_INIT_TOTAL_MAX,
    DP_INIT_SUBSISTENCE_MIN,
    DP_INIT_SUBSISTENCE_MAX,
)


def _get_terrain_sector_multipliers(terrain_type: str) -> dict:
    """Return the sector → multiplier dict for a terrain type (defaults to 1.0)."""
    return TERRAIN_TYPES.get(terrain_type, {}).get("multipliers", {})


def _distribute_dp(total: int, categories: list, weights: list) -> dict:
    """Distribute `total` DP across `categories` proportionally by `weights`.

    Uses largest-remainder rounding so the result always sums to `total`.

    Returns {category: dp_value}.
    """
    weight_sum = sum(weights)
    if weight_sum <= 0:
        # Fallback: equal distribution
        weight_sum = len(categories)
        weights = [1.0] * len(categories)

    raw = [total * w / weight_sum for w in weights]
    floored = [int(v) for v in raw]
    remainders = [(raw[i] - floored[i], i) for i in range(len(raw))]

    deficit = total - sum(floored)
    # Award remaining points to categories with the largest fractional parts.
    for _, idx in sorted(remainders, reverse=True)[:deficit]:
        floored[idx] += 1

    return {categories[i]: floored[i] for i in range(len(categories))}


def _province_dp_weights(terrain_type: str) -> list:
    """Compute per-building-category weights based on terrain sector multipliers.

    Categories whose parent sector has a high terrain multiplier get more DP.
    Categories with no mapped sector (unmapped categories) default to 1.0.
    """
    sector_mults = _get_terrain_sector_multipliers(terrain_type)
    weights = []
    for cat in DP_BUILDING_CATEGORIES:
        sector = BUILDING_CATEGORY_TO_SECTOR.get(cat)
        if sector is not None:
            weights.append(sector_mults.get(sector, 1.0))
        else:
            weights.append(1.0)
    return weights


def initialize_province_dp(game) -> None:
    """Initialize Development Points for all provinces and nations in a game.

    - Each province gets 100–200 non-subsistence DP distributed across all
      non-military building categories, weighted by terrain sector multipliers.
    - Each province also gets 20–40 subsistence DP (independent of terrain).
    - Each nation gets a NationDPPool (starts empty) and NationMilitaryDP rows
      for all three military categories (strategy/tactics/logistics), all at 0.
    - Uses bulk_create for efficiency.
    """
    from provinces.models import Province, ProvinceDevelopmentPoints
    from nations.models import Nation, NationDPPool, NationMilitaryDP

    provinces = list(Province.objects.filter(game=game))
    dp_rows = []

    for province in provinces:
        total = random.randint(DP_INIT_TOTAL_MIN, DP_INIT_TOTAL_MAX)
        subsistence_dp = random.randint(DP_INIT_SUBSISTENCE_MIN, DP_INIT_SUBSISTENCE_MAX)
        weights = _province_dp_weights(province.terrain_type)
        distribution = _distribute_dp(total, DP_BUILDING_CATEGORIES, weights)

        for cat, pts in distribution.items():
            dp_rows.append(ProvinceDevelopmentPoints(
                province=province, category=cat, points=pts
            ))
        dp_rows.append(ProvinceDevelopmentPoints(
            province=province, category="subsistence", points=subsistence_dp
        ))

    ProvinceDevelopmentPoints.objects.bulk_create(dp_rows, batch_size=500)

    # Nation-level DP pool and military DP stubs.
    nations = list(Nation.objects.filter(game=game))
    pool_rows = [NationDPPool(nation=n, available_points=0, last_grant_turn=0) for n in nations]
    NationDPPool.objects.bulk_create(pool_rows)

    military_rows = []
    for n in nations:
        for mil_cat in MILITARY_DP_CATEGORIES:
            military_rows.append(NationMilitaryDP(nation=n, category=mil_cat, points=0))
    NationMilitaryDP.objects.bulk_create(military_rows)
