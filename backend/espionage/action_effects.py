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


def apply_persuade_to_join(action, turn_number):
    """Apply the completion effect of a persuade_to_join action.

    Called when the action reaches its expires_turn. Assigns the target
    unclaimed province to the acting nation and begins normalization.

    If the province has already been claimed by the time the action
    completes, the action fails gracefully.
    """
    from economy.normalization import check_location_requirements, start_normalization

    province = action.target_province
    nation = action.nation

    if province is None:
        action.result["failed"] = "no_target_province"
        action.save(update_fields=["result"])
        logger.warning(f"persuade_to_join action {action.id}: no target province")
        return

    if province.nation_id is not None:
        # Province was claimed by someone else while the action was running.
        action.result["failed"] = "province_already_claimed"
        action.result["claimed_by"] = province.nation_id
        action.save(update_fields=["result"])
        logger.info(
            f"persuade_to_join: province {province.id} already claimed by "
            f"nation {province.nation_id}, action {action.id} failed"
        )
        return

    # Re-check location requirements in case geography changed.
    if not check_location_requirements(province, nation):
        action.result["failed"] = "location_requirements_no_longer_met"
        action.save(update_fields=["result"])
        logger.info(
            f"persuade_to_join: province {province.id} no longer meets location "
            f"requirements for nation {nation.id}"
        )
        return

    # Reconquest: if this nation is the province's original nation, skip normalization.
    if province.original_nation_id == nation.id:
        province.nation = nation
        province.is_core = True
        province.ideology_traits = nation.ideology_traits or {}
        province.normalization_started_turn = None
        province.normalization_duration = None
        province.save(update_fields=[
            "nation", "is_core", "ideology_traits",
            "normalization_started_turn", "normalization_duration",
        ])
        action.result["success"] = True
        action.result["reconquest"] = True
        action.save(update_fields=["result"])
        logger.info(
            f"persuade_to_join: province {province.id} reconquered by nation {nation.id} "
            f"(no normalization needed)"
        )
        return

    start_normalization(province, nation, turn_number)
    province.save(update_fields=[
        "nation", "is_core", "ideology_traits",
        "normalization_started_turn", "normalization_duration",
        "original_nation",
    ])
    action.result["success"] = True
    action.result["normalization_duration"] = province.normalization_duration
    action.save(update_fields=["result"])
    logger.info(
        f"persuade_to_join: province {province.id} joined nation {nation.id} "
        f"(normalization: {province.normalization_duration} turns)"
    )
