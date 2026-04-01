"""Effect implementations for active espionage actions.

Each function applies the per-turn (or one-shot) effect of an espionage action
to the target province / nation.  Called from simulation.py during the
espionage simulation step.
"""

import math
import logging

from .constants import ESPIONAGE_ACTION_DEFS

logger = logging.getLogger(__name__)


def apply_promote_foreign_ideology(action, province, transparency):
    """Apply per-turn instability effects of ideology promotion.

    Per turn while active:
      - province.local_stability -= 2.0 × (1.0 + transparency)
      - province.local_security  -= 1.0
      - Extra instability if province happiness < 40 or security < 30
    """
    defs = ESPIONAGE_ACTION_DEFS["promote_foreign_ideology"]

    stability_hit = defs["stability_per_turn"] * (1.0 + transparency)
    security_hit = defs["security_per_turn"]

    province.local_stability = max(0, province.local_stability + stability_hit)
    province.local_security = max(0, province.local_security + security_hit)

    # Extra instability in vulnerable provinces
    if province.local_happiness < 40 or province.local_security < 30:
        province.local_stability = max(
            0, province.local_stability + defs["extra_instability"]
        )

    province.save(update_fields=["local_stability", "local_security"])

    logger.info(
        f"Promote ideology: province {province.id} stability "
        f"{stability_hit:+.1f}, security {security_hit:+.1f}"
    )


def apply_terrorist_attack(action, province, turn_number):
    """Apply one-shot terrorist attack effects.

    - Kill ceil(population × 0.002) pops
    - Create a security penalty modifier lasting 3 turns
    """
    from nations.models import NationModifier

    defs = ESPIONAGE_ACTION_DEFS["terrorist_attack"]

    # Kill population
    killed = max(1, math.ceil(province.population * defs["pop_kill_fraction"]))
    province.population = max(0, province.population - killed)
    province.save(update_fields=["population"])

    # Apply security penalty via NationModifier on the target nation
    target_nation = action.target_nation
    NationModifier.objects.create(
        nation=target_nation,
        category="security_penalty",
        target=str(province.id),
        value=defs["security_penalty"],
        modifier_type=NationModifier.ModifierType.FLAT,
        source=NationModifier.Source.EVENT,
        expires_turn=turn_number + defs["security_penalty_duration"],
    )

    # Mark as executed so we don't re-apply
    action.result["executed"] = True
    action.result["killed"] = killed
    action.save(update_fields=["result"])

    logger.info(
        f"Terrorist attack: province {province.id} lost {killed} pops, "
        f"security penalty {defs['security_penalty']} for "
        f"{defs['security_penalty_duration']} turns"
    )


def apply_sabotage_building(action, province, transparency, turn_number):
    """Apply one-shot sabotage: disable a building for a computed number of turns.

    Disable duration = max(1, round(base + scale × transparency)) turns.
    """
    from provinces.models import Building

    defs = ESPIONAGE_ACTION_DEFS["sabotage_building"]

    target_building_type = action.target_building_type
    try:
        building = Building.objects.get(
            province=province,
            building_type=target_building_type,
            is_active=True,
        )
    except Building.DoesNotExist:
        action.result["executed"] = True
        action.result["failed"] = "building_not_found"
        action.save(update_fields=["result"])
        logger.warning(
            f"Sabotage failed: no active {target_building_type} in province {province.id}"
        )
        return

    disable_turns = max(
        1,
        round(defs["base_disable_turns"] + defs["transparency_disable_scale"] * transparency),
    )

    building.is_active = False
    building.save(update_fields=["is_active"])

    action.result["executed"] = True
    action.result["building_id"] = building.id
    action.result["re_enable_turn"] = turn_number + disable_turns
    action.save(update_fields=["result"])

    logger.info(
        f"Sabotage: disabled {target_building_type} in province {province.id} "
        f"for {disable_turns} turns (transparency={transparency:.2f})"
    )
