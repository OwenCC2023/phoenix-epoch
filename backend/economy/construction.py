"""
Construction queue processing.

Each constructible item type (buildings, military units, …) has its own
_tick_<type>(province, **kwargs) function.  process_construction_tick() calls
all of them in sequence, so adding a new type is always one function + one
append call — no other plumbing needed.

Each tick function returns the list of items that *completed* this turn so
callers (e.g. event logging) can react to completions.
"""


# ---------------------------------------------------------------------------
# Per-type tick functions
# ---------------------------------------------------------------------------

def _tick_buildings(province):
    """
    Advance construction timers for all buildings in a province.

    Returns the list of Building instances whose construction completed
    this tick (under_construction just became False).
    """
    completed = []
    for building in province.buildings.filter(under_construction=True):
        building.construction_turns_remaining = max(0, building.construction_turns_remaining - 1)
        if building.construction_turns_remaining == 0:
            building.under_construction = False
        building.save(update_fields=["under_construction", "construction_turns_remaining"])
        if not building.under_construction:
            completed.append(building)
    return completed


def get_province_base_synergy(province):
    """
    Return the total level sum of all active, completed military base buildings
    in a province (army_base + naval_base + air_base levels combined).

    Used to compute per-base training speed bonuses: each other base's levels
    contribute MILITARY_BASE_SYNERGY_BONUS to all other bases' training speed.
    """
    from provinces.military_constants import BASE_BUILDING_KEYS

    total = 0
    for building in province.buildings.all():
        if (
            building.building_type in BASE_BUILDING_KEYS
            and building.is_active
            and not building.under_construction
        ):
            total += building.level
    return total


def _tick_military_units(province, training_speed_bonus=0.0):
    """
    Advance training timers for all military units being trained in a province.

    Each turn a unit's construction_turns_remaining is reduced by:
        effective_reduction = 1.0 + synergy_bonus + training_speed_bonus

    where synergy_bonus = (other base levels) * MILITARY_BASE_SYNERGY_BONUS,
    capped at 0.50 (50% reduction per turn at most).

    training_speed_bonus comes from the Militarist trait and is passed in from
    the simulation loop.

    When training completes:
      - If the unit's formation is in the same province as training: units join
        directly (quantity += quantity_in_training).
      - Otherwise: units enter transit (quantity_in_transit += quantity_in_training).
        TODO: implement actual transit turns when combat system is designed.
        For now, transit is resolved instantly (units join formation immediately).

    Returns list of MilitaryUnit instances that completed training this tick.
    """
    from provinces.military_constants import (
        MILITARY_BASE_SYNERGY_BONUS,
        DOMAIN_TO_BASE,
        UNIT_TYPES,
    )
    from provinces.models import MilitaryUnit

    total_base_levels = get_province_base_synergy(province)
    completed = []

    units_in_training = MilitaryUnit.objects.filter(
        training_province=province,
        quantity_in_training__gt=0,
    ).select_related("formation__province")

    for unit in units_in_training:
        # Compute synergy: other bases' levels boost this unit's training speed.
        unit_def = UNIT_TYPES.get(unit.unit_type, {})
        domain = unit_def.get("domain", "")
        own_base_key = DOMAIN_TO_BASE.get(domain, "")
        own_level = 0
        for b in province.buildings.all():
            if b.building_type == own_base_key and b.is_active and not b.under_construction:
                own_level = b.level
                break
        other_levels = total_base_levels - own_level
        synergy_bonus = min(other_levels * MILITARY_BASE_SYNERGY_BONUS, 0.50)

        effective_reduction = 1.0 + synergy_bonus + training_speed_bonus
        unit.construction_turns_remaining = max(
            0.0, unit.construction_turns_remaining - effective_reduction
        )

        if unit.construction_turns_remaining <= 0:
            # Training complete.
            trained = unit.quantity_in_training
            formation_province_id = (
                unit.formation.province_id if unit.formation.province_id else None
            )
            if formation_province_id == province.id:
                # Same province: join formation directly.
                unit.quantity += trained
            else:
                # Different province: enter transit scaffold.
                # TODO: implement actual transit turns (combat system).
                unit.quantity_in_transit += trained
                unit.transit_turns_remaining = 0.0
                # Resolve instantly for now.
                unit.quantity += unit.quantity_in_transit
                unit.quantity_in_transit = 0

            unit.quantity_in_training = 0
            unit.construction_turns_remaining = 0.0
            unit.training_province = None
            completed.append(unit)

        unit.save(update_fields=[
            "quantity",
            "quantity_in_training",
            "construction_turns_remaining",
            "quantity_in_transit",
            "transit_turns_remaining",
            "training_province",
        ])

    return completed


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def process_construction_tick(province, training_speed_bonus=0.0):
    """
    Advance all construction timers in a province by one turn.

    Returns a list of (item_type: str, item) tuples for every project that
    completed this tick.  item_type is a human-readable label so callers can
    branch without importing every model.

    Parameters
    ----------
    training_speed_bonus : float
        Additive training speed bonus from Militarist trait effects.
        Passed through to _tick_military_units().

    To add a new constructible type:
        1. Implement _tick_<type>(province, …) → list[item]
        2. Append its results here.
    """
    completed = []

    for item in _tick_buildings(province):
        completed.append(("building", item))

    for item in _tick_military_units(province, training_speed_bonus=training_speed_bonus):
        completed.append(("military_unit", item))

    return completed


def get_nation_under_construction(nation):
    """
    Return all under-construction items for a nation, grouped by type.

    The returned dict uses the same type labels as process_construction_tick.

    Returns
    -------
    dict[str, list]
        e.g. {"buildings": [...], "military_units": [...]}
    """
    from provinces.models import Building, MilitaryUnit

    province_ids = nation.provinces.values_list("id", flat=True)

    buildings = (
        Building.objects
        .filter(province_id__in=province_ids, under_construction=True)
        .select_related("province")
        .order_by("province__name", "building_type")
    )

    units_in_training = (
        MilitaryUnit.objects
        .filter(
            training_province_id__in=province_ids,
            quantity_in_training__gt=0,
        )
        .select_related("formation", "training_province")
        .order_by("training_province__name", "unit_type")
    )

    return {
        "buildings": list(buildings),
        "military_units": list(units_in_training),
    }
