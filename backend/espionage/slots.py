"""Espionage slot capacity helpers.

Determines how many espionage operations a nation can run simultaneously
based on their intelligence buildings and their levels.
"""

from provinces.models import Building
from .models import BranchOfficeSpecialization, EspionageAction


def get_foreign_target_slots(nation):
    """Max simultaneous foreign nation targets = foreign_intel_hq level."""
    hq = Building.objects.filter(
        province__nation=nation,
        building_type="foreign_intel_hq",
        is_active=True,
        under_construction=False,
    ).first()
    return hq.level if hq else 0


def get_action_type_slots(nation, action_type):
    """Max simultaneous uses of a specific foreign action type.

    Each branch_office specialized in this action_type contributes
    its level as available slots.
    """
    total = 0
    specializations = BranchOfficeSpecialization.objects.filter(
        building__province__nation=nation,
        action_type=action_type,
    ).select_related("building")

    for spec in specializations:
        if spec.building.is_active and not spec.building.under_construction:
            total += spec.building.level
    return total


def get_suppress_slots(nation):
    """Max simultaneous suppress_foreign_operations actions = domestic_intel_hq level."""
    hq = Building.objects.filter(
        province__nation=nation,
        building_type="domestic_intel_hq",
        is_active=True,
        under_construction=False,
    ).first()
    return hq.level if hq else 0


def get_used_slots(nation, game):
    """Count active espionage actions grouped by type.

    Returns:
        dict with keys: "foreign_targets" (set of nation IDs), "by_type" (dict
        of action_type → count), "suppress" (int count of active suppress).
    """
    from .constants import FOREIGN_ACTION_TYPES

    active = EspionageAction.objects.filter(
        game=game,
        nation=nation,
        status=EspionageAction.Status.ACTIVE,
    )

    foreign_targets = set()
    by_type = {}
    suppress = 0

    for action in active:
        if action.action_type in FOREIGN_ACTION_TYPES:
            if action.target_nation_id:
                foreign_targets.add(action.target_nation_id)
            by_type[action.action_type] = by_type.get(action.action_type, 0) + 1
        elif action.action_type == EspionageAction.ActionType.SUPPRESS_FOREIGN_OPERATIONS:
            suppress += 1

    return {
        "foreign_targets": foreign_targets,
        "by_type": by_type,
        "suppress": suppress,
    }
