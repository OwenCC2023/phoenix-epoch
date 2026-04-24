"""Tax Efficiency (TE) computation.

TE is the fraction of the stated tax rate actually collected for a province,
applied to Income, Consumption, and Land taxes (NOT Gift/Estate — those are
point-of-transaction and administration-free).

    TE_province = TE_base + trait_mods + gov_mods + building_bonus(province)

where traits/gov/building contributions are additive (clamped to [0.01, 1.0]).
"""
from __future__ import annotations

from .tax_efficiency_constants import (
    TE_BASE,
    TE_BUILDING_BONUS_MAX,
    TE_BUILDING_BONUS_PER_LEVEL,
    TE_BUILDING_CATEGORIES,
    TE_MAX,
    TE_MIN,
)


def _clamp(v: float) -> float:
    return max(TE_MIN, min(TE_MAX, v))


def compute_nation_tax_efficiency_base(nation) -> float:
    """Return the nation-wide TE base (TE_BASE + traits + gov), no building bonus.

    Building bonus is per-province; add it on top via
    compute_province_tax_efficiency(base, province).
    """
    from .helpers import get_nation_trait_effects
    from .government_constants import get_combined_government_effects

    trait_effects = get_nation_trait_effects(nation) or {}
    trait_delta = float(trait_effects.get("tax_efficiency", 0.0))

    gov_effects = get_combined_government_effects(
        nation.gov_direction,
        nation.gov_economic_category,
        nation.gov_structure,
        nation.gov_power_origin,
        nation.gov_power_type,
    ) or {}
    gov_delta = float(gov_effects.get("tax_efficiency", 0.0))

    return _clamp(TE_BASE + trait_delta + gov_delta)


def _te_building_types() -> set[str]:
    """Resolve the set of building-type keys belonging to TE bonus categories."""
    from provinces.building_constants import BUILDING_TYPES
    return {
        key for key, defn in BUILDING_TYPES.items()
        if defn.get("category") in TE_BUILDING_CATEGORIES
    }


def compute_province_building_bonus(province) -> float:
    """Sum of active administrative-building levels in the province, scaled.

    Buildings counted: those in categories government_regulatory,
    government_management, government_oversight — only when active and
    fully constructed.
    """
    types = _te_building_types()
    total_levels = 0
    qs = province.buildings.filter(
        is_active=True,
        under_construction=False,
        building_type__in=types,
    )
    for b in qs:
        total_levels += int(b.level or 0)
    bonus = total_levels * TE_BUILDING_BONUS_PER_LEVEL
    return min(TE_BUILDING_BONUS_MAX, bonus)


def compute_province_tax_efficiency(nation_base: float, province) -> float:
    """Return TE for a specific province given the precomputed nation base."""
    return _clamp(nation_base + compute_province_building_bonus(province))
