"""
Control, Regions, and Rebellion System — control computation.

Control is a per-province value (1–100%) set by the player, either directly
on the province or via a Region (which pushes its control to all member
provinces). This module provides pure computation functions used during the
economy simulation and espionage simulation.
"""

import math
import statistics

from .control_constants import (
    CONTROL_MIN,
    CONTROL_MAX,
    PRODUCTION_BONUS_MAX,
    NORMALIZATION_DOUBLING_THRESHOLD,
    ESPIONAGE_TRANSPARENCY_BONUS_MAX,
    LIBERTARIAN_LOW_CONTROL_STABILITY_BONUS,
    LIBERTARIAN_LOW_CONTROL_HAPPINESS_BONUS,
    AUTHORITARIAN_UNHAPPY_PER_PCT,
    AUTHORITARIAN_UNHAPPY_CAP,
    EGALITARIAN_UNIFORMITY_BONUS,
)


# ---------------------------------------------------------------------------
# Effective control
# ---------------------------------------------------------------------------

def get_province_control(province) -> float:
    """Return the effective control for a province.

    If the province belongs to a Region, returns the region's control value
    (which was synced to province.control by sync_region_control at PATCH time).
    For provinces not in a region, returns province.control directly.

    Always returns a value in [CONTROL_MIN, CONTROL_MAX].
    """
    return max(CONTROL_MIN, min(CONTROL_MAX, province.control))


# ---------------------------------------------------------------------------
# Core economic formulas
# ---------------------------------------------------------------------------

def control_tax_multiplier(control: float) -> float:
    """Per-province tax efficiency multiplier based on control (STUB).

    Wealth & Taxation System hook — low-control provinces collect less tax.
    Currently returns 1.0 unconditionally; tune curve when the Control System
    is extended.  See docs/future_systems.md.
    """
    return 1.0


def compute_national_flow_fraction(control: float) -> float:
    """Fraction of province surplus that reaches the national government.

    Formula: control / 100.0
    At 100% control → 1.0 (all surplus flows nationally)
    At  1% control  → 0.01 (almost nothing flows nationally)
    """
    return control / 100.0


def compute_production_bonus(control: float) -> float:
    """Production multiplier bonus from loosened control.

    Lower control lets local producers operate with less interference.
    Applies to materials, energy, and kapital only (not food or manpower).

    Formula: PRODUCTION_BONUS_MAX * (1 - control/100)
    At 100% control → 0.0  (no bonus)
    At  60% control → 0.10 (+10%)
    At   1% control → ~0.2475 (~+25%)
    """
    return PRODUCTION_BONUS_MAX * (1.0 - control / 100.0)


def compute_normalization_control_multiplier(control: float) -> float:
    """Normalization time multiplier based on control level.

    For every NORMALIZATION_DOUBLING_THRESHOLD percentage points below 100%,
    normalization duration doubles.

    Formula: 2 ** ((100 - control) / NORMALIZATION_DOUBLING_THRESHOLD)
    At 100% control → 1.0×  (no change)
    At  60% control → 2.0×  (double the time)
    At  20% control → 4.0×  (quadruple the time)
    At   1% control → ~5.3× (more than 5× the time)
    """
    return 2.0 ** ((100.0 - control) / NORMALIZATION_DOUBLING_THRESHOLD)


# ---------------------------------------------------------------------------
# Espionage effects
# ---------------------------------------------------------------------------

def compute_espionage_defense_multiplier(avg_control: float) -> float:
    """Multiplier applied to national espionage defense based on control.

    Lower control means less government presence, weaker defense.
    Applied as a multiplier to the computed national_defense value.

    Formula: control / 100.0 (same as national_flow_fraction)
    """
    return max(0.01, avg_control / 100.0)


def compute_espionage_transparency_bonus(avg_control: float) -> float:
    """Additional transparency score granted to foreign intelligence due to
    weak central governance in the target nation.

    Formula: ESPIONAGE_TRANSPARENCY_BONUS_MAX * (1 - control/100)
    At 100% control → 0.0  (no bonus for attackers)
    At   1% control → ~0.30 (full bonus)
    """
    return ESPIONAGE_TRANSPARENCY_BONUS_MAX * (1.0 - avg_control / 100.0)


# ---------------------------------------------------------------------------
# Ideology-control interactions
# ---------------------------------------------------------------------------

def compute_libertarian_control_bonus(
    control: float, is_strong: bool
) -> tuple[float, float]:
    """Return (stability_bonus, happiness_bonus) for a Libertarian province.

    Libertarians enjoy more freedom when control is lower.
    Strong trait receives the full bonus; weak trait receives half.

    Parameters
    ----------
    control : float
        Effective control level for the province (1–100).
    is_strong : bool
        True if libertarian is the strong trait; False if weak.

    Returns
    -------
    (stability_bonus, happiness_bonus) : (float, float)
        Both are positive values to ADD to the province's stability/happiness.
    """
    scale = 1.0 if is_strong else 0.5
    factor = 1.0 - control / 100.0
    stab_bonus = LIBERTARIAN_LOW_CONTROL_STABILITY_BONUS * factor * scale
    hap_bonus = LIBERTARIAN_LOW_CONTROL_HAPPINESS_BONUS * factor * scale
    return stab_bonus, hap_bonus


def compute_authoritarian_national_penalty(
    province_controls: list[float], is_strong: bool
) -> float:
    """National happiness penalty for Authoritarian nations with low-control provinces.

    Authoritarians disapprove of any province operating below full control.
    Each province below 100% contributes a penalty; total is capped.

    Parameters
    ----------
    province_controls : list[float]
        Effective control level for each province.
    is_strong : bool
        True if authoritarian is the strong trait; False if weak.

    Returns
    -------
    float
        Positive value to SUBTRACT from national happiness.
    """
    scale = 1.0 if is_strong else 0.5
    total = sum(
        AUTHORITARIAN_UNHAPPY_PER_PCT * (100.0 - c) / 100.0
        for c in province_controls
        if c < 100.0
    )
    return min(AUTHORITARIAN_UNHAPPY_CAP, total) * scale


def compute_egalitarian_national_bonus(
    province_controls: list[float], is_strong: bool
) -> float:
    """National happiness bonus for Egalitarian nations with uniform control.

    Egalitarians prefer that all provinces are treated equally. The bonus is
    highest when all provinces have identical control levels.

    Parameters
    ----------
    province_controls : list[float]
        Effective control level for each province.
    is_strong : bool
        True if egalitarian is the strong trait; False if weak.

    Returns
    -------
    float
        Positive value to ADD to national happiness.
    """
    if len(province_controls) < 2:
        return EGALITARIAN_UNIFORMITY_BONUS * (1.0 if is_strong else 0.5)

    scale = 1.0 if is_strong else 0.5
    stdev = statistics.stdev(province_controls)
    # stdev of 0 → full bonus; stdev of 50 → 0 bonus; stdev > 50 → clamped at 0
    uniformity = max(0.0, 1.0 - stdev / 50.0)
    return EGALITARIAN_UNIFORMITY_BONUS * uniformity * scale


# ---------------------------------------------------------------------------
# Region control sync
# ---------------------------------------------------------------------------

def sync_region_control(region) -> list:
    """Push region.control to all member provinces.

    Called when a region's control is updated via the API. Denormalizes the
    control value onto Province.control to keep the simulation loop
    join-free.

    Returns the list of modified Province objects (caller must bulk_update
    or save them).
    """
    provinces = list(region.provinces.all())
    for province in provinces:
        province.control = region.control
    return provinces
