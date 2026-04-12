"""Per-turn espionage simulation.

Called after the economy simulation each turn. Computes Attack, Defense,
and Transparency for all nation pairs, applies action effects, and
updates EspionageState rows.
"""

import logging

from .computation import (
    compute_national_attack,
    compute_national_defense,
    compute_provincial_defense,
    compute_transparency,
)
from .constants import ESPIONAGE_ACTION_DEFS
from .models import EspionageAction, EspionageState, IntelligenceSharing
from .revelation import compute_revealed_info

logger = logging.getLogger(__name__)


def simulate_espionage(game, turn_number):
    """Run the espionage simulation for all nations in a game.

    1. Pre-compute per-nation data (traits, policies, buildings, stability).
    2. For each (attacker, target) pair: compute attack, defense, transparency,
       and revealed info. Upsert EspionageState.
    3. Apply active action effects (ideology promotion, terrorist attacks,
       sabotage, building re-enables).
    4. Expire completed actions.
    """
    from nations.models import Nation, NationPolicy
    from nations.helpers import get_nation_trait_effects
    from nations.policy_effects import get_nation_policy_effects
    from economy.building_simulation import get_national_building_effects, get_province_building_effects
    from economy.models import NationResourcePool

    alive_nations = list(Nation.objects.filter(game=game, is_alive=True))
    if len(alive_nations) < 2:
        return

    # --- Step 1: Pre-compute per-nation data ---
    nation_data = {}
    for nation in alive_nations:
        provinces = list(nation.provinces.all())

        trait_effects = get_nation_trait_effects(nation)
        policy_effects = get_nation_policy_effects(nation)
        national_bldg = get_national_building_effects(provinces)

        # Active policies as {category: level}
        active_policies = dict(
            NationPolicy.objects.filter(nation=nation).values_list("category", "level")
        )

        # FIA policy level
        fia_level = active_policies.get("foreign_intelligence_agency", 0)

        # National stability
        try:
            pool = NationResourcePool.objects.get(nation=nation)
            stability = pool.stability
        except NationResourcePool.DoesNotExist:
            stability = 50.0

        # espionage_bonus and counter_espionage_bonus from traits + policies
        espionage_bonus = (
            trait_effects.get("espionage_bonus", 0.0)
            + policy_effects.get("espionage_bonus", 0.0)
        )
        counter_espionage_bonus = (
            trait_effects.get("counter_espionage_bonus", 0.0)
            + policy_effects.get("counter_espionage_bonus", 0.0)
        )

        # Province-level building effects (for provincial defense)
        province_bldg_effects = {}
        for prov in provinces:
            province_bldg_effects[prov.id] = get_province_building_effects(prov)

        # Suppress actions for provincial defense
        suppress_provinces = set(
            EspionageAction.objects.filter(
                game=game,
                nation=nation,
                action_type=EspionageAction.ActionType.SUPPRESS_FOREIGN_OPERATIONS,
                status=EspionageAction.Status.ACTIVE,
            ).values_list("target_province_id", flat=True)
        )

        nation_data[nation.id] = {
            "nation": nation,
            "provinces": provinces,
            "ideology_traits": nation.ideology_traits or {},
            "trait_effects": trait_effects,
            "policy_effects": policy_effects,
            "national_bldg": national_bldg,
            "active_policies": active_policies,
            "fia_level": fia_level,
            "stability": stability,
            "espionage_bonus": espionage_bonus,
            "counter_espionage_bonus": counter_espionage_bonus,
            "province_bldg_effects": province_bldg_effects,
            "suppress_provinces": suppress_provinces,
            "literacy": 0,  # stub until literacy system is wired
        }

    # --- Step 2: Compute attack/defense/transparency per pair ---
    for attacker in alive_nations:
        a_data = nation_data[attacker.id]
        for target in alive_nations:
            if attacker.id == target.id:
                continue

            t_data = nation_data[target.id]

            # Stability advantages
            stability_adv_attack = a_data["stability"] - t_data["stability"]
            stability_adv_defense = t_data["stability"] - a_data["stability"]
            literacy_adv_defense = t_data["literacy"] - a_data["literacy"]

            national_attack = compute_national_attack(
                fia_policy_level=a_data["fia_level"],
                building_attack=a_data["national_bldg"].get("espionage_attack", 0.0),
                espionage_bonus=a_data["espionage_bonus"],
                ideology_traits=a_data["ideology_traits"],
                stability_advantage=stability_adv_attack,
            )

            national_defense = compute_national_defense(
                building_defense=t_data["national_bldg"].get("espionage_defense", 0.0),
                counter_espionage_bonus=t_data["counter_espionage_bonus"],
                active_policies=t_data["active_policies"],
                ideology_traits=t_data["ideology_traits"],
                stability_advantage=stability_adv_defense,
                literacy_advantage=literacy_adv_defense,
            )

            transparency = compute_transparency(national_attack, national_defense)

            # Check for investigate_province actions — per-province transparency boost
            investigate_actions = EspionageAction.objects.filter(
                game=game,
                nation=attacker,
                target_nation=target,
                action_type=EspionageAction.ActionType.INVESTIGATE_PROVINCE,
                status=EspionageAction.Status.ACTIVE,
            )

            # Voluntary shares
            shared_cats = set(
                IntelligenceSharing.objects.filter(
                    game=game,
                    source_nation=target,
                    viewer_nation=attacker,
                    is_shared=True,
                ).values_list("category", flat=True)
            )

            # Compute revealed info
            revealed = compute_revealed_info(
                transparency=transparency,
                target_nation=target,
                game=game,
                voluntary_shares=shared_cats,
            )

            # Apply investigate_province per-province transparency overrides
            investigate_bonus = ESPIONAGE_ACTION_DEFS["investigate_province"]["attack_bonus"]
            for action in investigate_actions:
                if action.target_province_id:
                    prov_bldg = t_data["province_bldg_effects"].get(
                        action.target_province_id, {}
                    )
                    suppress_bonus = (
                        ESPIONAGE_ACTION_DEFS["suppress_foreign_operations"]["defense_bonus"]
                        if action.target_province_id in t_data["suppress_provinces"]
                        else 0
                    )
                    prov_defense = compute_provincial_defense(
                        national_defense,
                        prov_bldg.get("provincial_espionage_defense", 0.0),
                        suppress_bonus,
                    )
                    boosted_attack = national_attack + investigate_bonus
                    prov_transparency = compute_transparency(boosted_attack, prov_defense)
                    # Store per-province override in revealed info
                    revealed.setdefault("_investigate_overrides", {})[
                        str(action.target_province_id)
                    ] = round(prov_transparency, 4)

            # Upsert EspionageState
            state, created = EspionageState.objects.update_or_create(
                game=game,
                attacker=attacker,
                target=target,
                defaults={
                    "national_attack": round(national_attack, 2),
                    "national_defense": round(national_defense, 2),
                    "transparency": round(transparency, 4),
                    "revealed_info": revealed,
                    "turn_updated": turn_number,
                },
            )

    # --- Step 3: Apply active action effects ---
    _apply_action_effects(game, turn_number, nation_data)

    # --- Step 4: Apply persuade_to_join completion effects, then expire all others ---
    _complete_persuade_actions(game, turn_number)
    _expire_actions(game, turn_number)

    # --- Step 5: Re-enable sabotaged buildings ---
    _reenable_sabotaged_buildings(game, turn_number)


def _apply_action_effects(game, turn_number, nation_data):
    """Apply effects of active espionage actions."""
    from .action_effects import (
        apply_promote_foreign_ideology,
        apply_terrorist_attack,
        apply_sabotage_building,
    )

    active_actions = EspionageAction.objects.filter(
        game=game,
        status=EspionageAction.Status.ACTIVE,
    ).select_related("target_province", "target_nation")

    for action in active_actions:
        if action.action_type == EspionageAction.ActionType.PROMOTE_FOREIGN_IDEOLOGY:
            if action.target_province:
                # Get transparency for this pair
                try:
                    state = EspionageState.objects.get(
                        game=game,
                        attacker=action.nation,
                        target=action.target_nation,
                    )
                    t = state.transparency
                except EspionageState.DoesNotExist:
                    t = 0.0
                apply_promote_foreign_ideology(action, action.target_province, t)

        elif action.action_type == EspionageAction.ActionType.TERRORIST_ATTACK:
            if action.target_province and not action.result.get("executed"):
                try:
                    state = EspionageState.objects.get(
                        game=game,
                        attacker=action.nation,
                        target=action.target_nation,
                    )
                    t = state.transparency
                except EspionageState.DoesNotExist:
                    t = 0.0
                apply_terrorist_attack(action, action.target_province, turn_number)

        elif action.action_type == EspionageAction.ActionType.SABOTAGE_BUILDING:
            if action.target_province and not action.result.get("executed"):
                try:
                    state = EspionageState.objects.get(
                        game=game,
                        attacker=action.nation,
                        target=action.target_nation,
                    )
                    t = state.transparency
                except EspionageState.DoesNotExist:
                    t = 0.0
                apply_sabotage_building(action, action.target_province, t, turn_number)


def _complete_persuade_actions(game, turn_number):
    """Apply completion effects for persuade_to_join actions that have reached expiry.

    Must run BEFORE _expire_actions so the actions are still ACTIVE when we
    apply their effects. After applying, marks each action as COMPLETED.
    """
    from .action_effects import apply_persuade_to_join

    completing = EspionageAction.objects.filter(
        game=game,
        action_type=EspionageAction.ActionType.PERSUADE_TO_JOIN,
        status=EspionageAction.Status.ACTIVE,
        expires_turn__lte=turn_number,
    ).select_related("target_province", "nation")

    for action in completing:
        apply_persuade_to_join(action, turn_number)
        action.status = EspionageAction.Status.COMPLETED
        action.save(update_fields=["status", "result"])


def _expire_actions(game, turn_number):
    """Mark non-persuade actions past their expiry turn as completed."""
    expired = EspionageAction.objects.filter(
        game=game,
        status=EspionageAction.Status.ACTIVE,
        expires_turn__lte=turn_number,
    ).exclude(action_type=EspionageAction.ActionType.PERSUADE_TO_JOIN)
    count = expired.update(status=EspionageAction.Status.COMPLETED)
    if count:
        logger.info(f"Expired {count} espionage actions in game {game.id}")


def _reenable_sabotaged_buildings(game, turn_number):
    """Re-enable buildings whose sabotage timer has expired."""
    from provinces.models import Building

    sabotaged = EspionageAction.objects.filter(
        game=game,
        action_type=EspionageAction.ActionType.SABOTAGE_BUILDING,
        status=EspionageAction.Status.COMPLETED,
    )

    for action in sabotaged:
        re_enable_turn = action.result.get("re_enable_turn")
        building_id = action.result.get("building_id")
        if re_enable_turn and building_id and turn_number >= re_enable_turn:
            try:
                building = Building.objects.get(pk=building_id)
                if not building.is_active:
                    building.is_active = True
                    building.save(update_fields=["is_active"])
                    logger.info(
                        f"Re-enabled sabotaged building {building.building_type} "
                        f"in province {building.province_id}"
                    )
            except Building.DoesNotExist:
                pass
            # Clear the result so we don't re-process
            action.result = {}
            action.save(update_fields=["result"])
