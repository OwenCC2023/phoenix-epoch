"""
Economy simulation engine.
Runs each turn to calculate province production, national rollup, and updates.
"""
from django.db import transaction

from .constants import (
    BASE_INTEGRATION_EFFICIENCY,
    FOOD_CONSUMPTION_PER_POP,
    STABILITY_FOOD_DEFICIT_PENALTY,
    STABILITY_RECOVERY_RATE,
)
from .models import NationResourcePool, ResourceLedger, ProvinceLedger
from .building_simulation import (
    simulate_building_production,
    simulate_good_consumption,
    get_province_building_effects,
    get_national_building_effects,
    get_building_efficiency_modifiers,
)
from .construction import process_construction_tick
from .population import (
    calculate_province_growth_rate,
    simulate_migration,
    simulate_economic_migration,
)
from .security import (
    compute_province_security,
    get_security_stability_multiplier,
    get_security_growth_bonus,
)
from .happiness import (
    compute_province_happiness,
    get_happiness_growth_multiplier,
    get_happiness_stability_recovery_multiplier,
)
from .literacy import (
    compute_literacy_growth,
    get_national_literacy,
    get_literacy_research_multiplier,
)
from .normalization import (
    check_normalization_completion,
    compute_normalization_penalties,
)
from .whitespace import simulate_all_whitespace
from .control import (
    get_province_control,
    compute_production_bonus,
    compute_national_flow_fraction,
    compute_libertarian_control_bonus,
    compute_authoritarian_national_penalty,
    compute_egalitarian_national_bonus,
)


RESOURCE_KEYS = ["food", "materials", "energy", "wealth", "manpower", "research"]


def empty_resources():
    return {k: 0.0 for k in RESOURCE_KEYS}


def _get_rationing_level(nation):
    """Return the nation's rationing policy level (0 = no_rationing, 1-3 = priority)."""
    from nations.models import NationPolicy
    try:
        policy = NationPolicy.objects.get(nation=nation, category="rationing")
        return policy.current_level
    except NationPolicy.DoesNotExist:
        return 0


def _compute_unit_needs(nation, trait_effects):
    """
    Compute total upkeep needs for all active military units in the nation,
    with upkeep_reduction already applied.

    Returns a dict of {good: total_amount} for use by the rationing system.
    """
    from provinces.military_constants import UNIT_TYPES
    from provinces.models import MilitaryUnit

    upkeep_reduction = min(0.75, trait_effects.get("military_upkeep_reduction", 0.0))
    active_units = MilitaryUnit.objects.filter(
        formation__nation=nation, quantity__gt=0
    )
    needs = {}
    for unit in active_units:
        unit_def = UNIT_TYPES.get(unit.unit_type, {})
        upkeep = unit_def.get("upkeep", {})
        scale = unit.quantity * (1.0 - upkeep_reduction)
        for good, amount in upkeep.items():
            needs[good] = needs.get(good, 0.0) + amount * scale
    return needs


def simulate_economy_for_game(game, turn_number):
    """Run the full economy simulation for all nations in a game."""
    from nations.models import Nation
    from provinces.models import Province
    from trade.simulation import recompute_route_paths

    # Recompute all trade route paths for this game before running per-nation economy.
    # This ensures capital movements and adjacency changes are reflected in exports.
    recompute_route_paths(game, turn_number)

    nations = Nation.objects.filter(game=game, is_alive=True).prefetch_related(
        "provinces__buildings",
        "provinces__resources",
        "modifiers",
    )

    for nation in nations:
        simulate_nation_economy(nation, turn_number)

    # Simulate whitespace provinces (nation=None): de-integration, melding, drift.
    simulate_all_whitespace(game, turn_number)


@transaction.atomic
def simulate_nation_economy(nation, turn_number):
    """Full economy simulation for a single nation."""
    from provinces.models import ProvinceResources
    from provinces.constants import TERRAIN_TYPES
    from provinces.jobs import (
        get_province_job_status,
        calculate_province_designation,
        terrain_primary_resource,
        terrain_best_multiplier,
        SUBSISTENCE_RATE,
        MANPOWER_PER_POP,
    )
    from provinces.constants import DESIGNATION_SUBSISTENCE_MODIFIERS

    provinces = list(nation.provinces.all())
    if not provinces:
        return

    # Pre-compute total population (needed for food stability supplement below)
    total_pop = sum(p.population for p in provinces)

    # Gather national modifiers
    national_modifiers = _gather_national_modifiers(nation, turn_number)

    # Gather trait effects (direct lookup, not via NationModifier)
    from nations.helpers import get_nation_trait_effects
    trait_effects = get_nation_trait_effects(nation)

    # Gather policy effects (context-dependent on government/traits)
    from nations.policy_effects import get_nation_policy_effects
    policy_effects = get_nation_policy_effects(nation)

    # Bureaucratic capacity: supply vs demand.
    # If demand exceeds supply, reduce positive policy effects proportionally
    # (most expensive policies lose benefits first) and track stability penalty.
    from nations.bureaucratic_capacity import (
        compute_bureaucratic_supply,
        compute_total_bureaucratic_demand,
        compute_bureaucratic_deficit_penalties,
        apply_deficit_to_policy_effects,
    )
    bc_supply = compute_bureaucratic_supply(nation, provinces)
    bc_demand = compute_total_bureaucratic_demand(nation)
    bc_stability_penalty = 0.0
    if bc_demand["total"] > bc_supply["total"]:
        bc_penalties = compute_bureaucratic_deficit_penalties(
            bc_supply["total"], bc_demand["total"], bc_demand["per_policy"]
        )
        bc_stability_penalty = bc_penalties["stability_penalty"]
        policy_effects = apply_deficit_to_policy_effects(
            policy_effects, bc_penalties["global_benefit_factor"]
        )

    # Apply trait + policy bonuses to national modifiers.
    # Both old-style keys (integration_bonus, research_bonus) and new-style
    # keys (integration_pct, research_pct) are checked and summed.
    # Security system: pre-compute nation-level multipliers once per turn.
    from nations.policy_effects import get_security_policy_multiplier
    security_policy_mult = get_security_policy_multiplier(nation)
    security_trait_mult = trait_effects.get("security_multiplier", 1.0)
    ideology_traits = nation.ideology_traits or {}
    all_trait_keys = set()
    if ideology_traits.get("strong"):
        all_trait_keys.add(ideology_traits["strong"])
    all_trait_keys.update(ideology_traits.get("weak", []))
    has_internationalist = "internationalist" in all_trait_keys
    # Control-ideology interactions (pre-computed once per nation)
    _strong_trait = ideology_traits.get("strong")
    is_libertarian_strong = _strong_trait == "libertarian"
    is_libertarian = "libertarian" in all_trait_keys
    is_authoritarian_strong = _strong_trait == "authoritarian"
    is_authoritarian = "authoritarian" in all_trait_keys
    is_egalitarian_strong = _strong_trait == "egalitarian"
    is_egalitarian = "egalitarian" in all_trait_keys

    integration_bonus_from_traits = (
        trait_effects.get("integration_bonus", 0.0)
        + trait_effects.get("integration_pct", 0.0)
        + policy_effects.get("integration_bonus", 0.0)
        + policy_effects.get("integration_pct", 0.0)
    )
    stability_bonus_from_traits = (
        trait_effects.get("stability_bonus", 0.0) + trait_effects.get("stability_penalty", 0.0)
        + policy_effects.get("stability_bonus", 0.0) + policy_effects.get("stability_penalty", 0.0)
    )
    growth_bonus_from_traits = (
        trait_effects.get("growth_bonus", 0.0) + trait_effects.get("growth_penalty", 0.0)
        + trait_effects.get("growth_rate", 0.0)
        + policy_effects.get("growth_bonus", 0.0) + policy_effects.get("growth_penalty", 0.0)
        + policy_effects.get("growth_rate", 0.0)
    )
    research_mod_from_traits = (
        trait_effects.get("research_bonus", 0.0) + trait_effects.get("research_penalty", 0.0)
        + trait_effects.get("research_pct", 0.0)
        + policy_effects.get("research_bonus", 0.0) + policy_effects.get("research_penalty", 0.0)
        + policy_effects.get("research_pct", 0.0)
    )
    manpower_mod_from_traits = (
        trait_effects.get("manpower_bonus", 0.0)
        + policy_effects.get("manpower_bonus", 0.0)
    )
    wealth_mod_from_traits = (
        trait_effects.get("wealth_production_bonus", 0.0)
        + trait_effects.get("production_wealth_pct", 0.0)
        + policy_effects.get("wealth_production_bonus", 0.0)
        + policy_effects.get("production_wealth_pct", 0.0)
    )
    food_mod_from_traits = (
        trait_effects.get("food_production_bonus", 0.0)
        + trait_effects.get("production_food_pct", 0.0)
        + policy_effects.get("food_production_bonus", 0.0)
        + policy_effects.get("production_food_pct", 0.0)
    )
    upkeep_reduction_from_traits = (
        trait_effects.get("upkeep_reduction", 0.0)
        + policy_effects.get("upkeep_reduction", 0.0)
    )

    # New effect columns — tracked for downstream use
    worker_productivity = (
        trait_effects.get("worker_productivity", 0.0)
        + policy_effects.get("worker_productivity", 0.0)
    )
    corruption_resistance = (
        trait_effects.get("corruption_resistance", 0.0)
        + policy_effects.get("corruption_resistance", 0.0)
    )
    environmental_health = (
        trait_effects.get("environmental_health", 0.0)
        + policy_effects.get("environmental_health", 0.0)
    )

    integration_modifier = BASE_INTEGRATION_EFFICIENCY + national_modifiers.get("integration", 0) + integration_bonus_from_traits
    integration_modifier = max(0.5, min(1.0, integration_modifier))

    # Fetch pool now so we can use last turn's food stockpile for stability checks.
    pool, _ = NationResourcePool.objects.get_or_create(nation=nation)

    total_province_production = empty_resources()
    total_integration_losses = empty_resources()
    total_local_consumption = empty_resources()
    total_exported = empty_resources()

    # Per-province snapshots used by later steps.
    province_food = {}        # id → (food_produced, food_needed)
    province_job_status = {}  # id → job status dict
    province_controls = []    # list of effective control values (for national ideology effects)

    # National building effects (upkeep_reduction, construction_cost_reduction)
    national_bldg_effects = get_national_building_effects(provinces)
    upkeep_reduction = min(0.75, national_bldg_effects.get("upkeep_reduction", 0.0))

    # Pre-compute active policies dict for happiness calculation (same for all provinces)
    from nations.models import NationPolicy
    active_policies = {p.category: p.current_level for p in NationPolicy.objects.filter(nation=nation)}

    # Pre-compute DP multipliers per province per building category (System 17).
    from provinces.models import ProvinceDevelopmentPoints
    from .dp import compute_province_dp_multipliers
    province_dp_data = {}  # province_id -> {category: dp_value}
    for dp_row in ProvinceDevelopmentPoints.objects.filter(province__in=provinces):
        province_dp_data.setdefault(dp_row.province_id, {})[dp_row.category] = dp_row.points
    province_dp_multipliers = {
        pid: compute_province_dp_multipliers(dp_dict)
        for pid, dp_dict in province_dp_data.items()
    }

    for province in provinces:
        # ----------------------------------------------------------------
        # Step 1: Determine employment split via job system
        # ----------------------------------------------------------------
        job_status = get_province_job_status(province)
        province_job_status[province.id] = job_status

        # ----------------------------------------------------------------
        # Step 2: Province building effects
        #   Compute additive multipliers/bonuses from active buildings.
        # ----------------------------------------------------------------
        bldg_effects = get_province_building_effects(province)

        # Effective control level for this province (used in Steps 3, 5, 6).
        province_control = get_province_control(province)
        province_controls.append(province_control)

        # ----------------------------------------------------------------
        # Step 3: Subsistence production
        #   All workers not in buildings produce the terrain's primary
        #   resource.  Manpower has a small population-based baseline.
        #   Designation (rural/urban/post_urban) modifies output.
        #   farming_bonus and research_bonus from buildings apply here.
        # ----------------------------------------------------------------
        primary = terrain_primary_resource(province.terrain_type)
        best_mult = terrain_best_multiplier(province.terrain_type)
        urban_threshold_reduction = trait_effects.get("urban_threshold_reduction", 0)
        designation = calculate_province_designation(province, urban_threshold_reduction)
        desg_mods = DESIGNATION_SUBSISTENCE_MODIFIERS[designation]

        farming_mult = 1.0 + bldg_effects.get("farming_bonus", 0.0)
        research_mult = 1.0 + bldg_effects.get("research_bonus", 0.0)

        raw_production = empty_resources()
        base_primary = round(
            job_status["subsistence_workers"] * SUBSISTENCE_RATE * best_mult
            * desg_mods.get(primary, 1.0),
            2,
        )
        # Apply building bonus multipliers to the primary resource.
        if primary == "food":
            raw_production[primary] = round(base_primary * farming_mult, 2)
        elif primary == "research":
            raw_production[primary] = round(base_primary * research_mult, 2)
        else:
            raw_production[primary] = base_primary

        # Apply trait-based designation bonuses to subsistence output
        if designation == "rural":
            rural_bonus = trait_effects.get("rural_output_bonus", 0.0)
            rural_penalty = trait_effects.get("rural_output_penalty", 0.0)
            trait_mult = 1.0 + rural_bonus + rural_penalty
            if trait_mult != 1.0:
                raw_production[primary] = round(raw_production[primary] * trait_mult, 2)

        # Apply trait food production bonus (e.g. traditionalist)
        if primary == "food" and food_mod_from_traits:
            raw_production["food"] = round(raw_production["food"] * (1.0 + food_mod_from_traits), 2)

        # Apply trait research modifier
        if primary == "research" and research_mod_from_traits:
            raw_production["research"] = round(raw_production["research"] * (1.0 + research_mod_from_traits), 2)

        # Apply subsistence DP multiplier (System 17 — multiplier of multipliers)
        sub_dp_mult = province_dp_multipliers.get(province.id, {}).get("subsistence", 1.0)
        if sub_dp_mult != 1.0:
            raw_production[primary] = round(raw_production[primary] * sub_dp_mult, 2)

        raw_production["manpower"] = round(
            province.population * MANPOWER_PER_POP * desg_mods.get("manpower", 1.0)
            * (1.0 + manpower_mod_from_traits),
            2,
        )

        if province.is_rebel_occupied:
            # Rebels have seized the province — no production reaches the nation.
            raw_production = empty_resources()
        else:
            # Control production bonus applies to materials, energy, wealth only.
            prod_bonus = compute_production_bonus(province_control)
            if prod_bonus > 0:
                for key in ("materials", "energy", "wealth"):
                    raw_production[key] = round(raw_production[key] * (1.0 + prod_bonus), 2)

        # ----------------------------------------------------------------
        # Step 4: Local consumption (food for population)
        # ----------------------------------------------------------------
        local_food_consumption = province.population * FOOD_CONSUMPTION_PER_POP
        local_consumption = empty_resources()
        local_consumption["food"] = round(local_food_consumption, 2)

        # ----------------------------------------------------------------
        # Step 5: Province surplus → exported to nation (with integration and control)
        #   integration_bonus from buildings adds to per-province integration.
        #   control_flow gates how much of the surplus reaches the national pool.
        #   Rebel-occupied provinces export nothing (and contribute no deficits).
        # ----------------------------------------------------------------
        province_integration = min(1.0, integration_modifier + bldg_effects.get("integration_bonus", 0.0))
        exported = empty_resources()
        if not province.is_rebel_occupied:
            control_flow = compute_national_flow_fraction(province_control)
            for key in RESOURCE_KEYS:
                surplus = raw_production[key] - local_consumption.get(key, 0)
                if surplus > 0:
                    exported[key] = round(surplus * province_integration * control_flow, 2)
                else:
                    exported[key] = round(surplus, 2)  # deficit passes through fully

        # Store food data for growth calculation (after final pool is known)
        province_food[province.id] = (raw_production["food"], local_consumption["food"])

        # ----------------------------------------------------------------
        # Step 6: Province stability — considers national food supplement
        #   Uses previous turn's pool.food so non-food provinces aren't
        #   perpetually penalised when the nation has a healthy stockpile.
        #   stability_recovery_bonus from buildings adds to recovery rate.
        #   Security multiplies the effective recovery (high security = faster recovery).
        #   Rebel-occupied provinces receive no national food distribution.
        # ----------------------------------------------------------------
        if province.is_rebel_occupied:
            effective_food = 0.0  # rebels cut off national food distribution
        else:
            national_food_share = (pool.food / max(total_pop, 1)) * province.population
            effective_food = raw_production["food"] + national_food_share
        food_ratio = effective_food / max(local_food_consumption, 0.001)

        # Step 6a: Province security (computed fresh each turn)
        province.local_security = compute_province_security(
            bldg_effects=bldg_effects,
            policy_security_mult=security_policy_mult,
            trait_security_mult=security_trait_mult,
            food_ratio=food_ratio,
            net_immigration_pct=0.0,  # immigration penalty wired in Step 13b-c
            has_internationalist=has_internationalist,
        )

        security_stability_mult = get_security_stability_multiplier(province.local_security)

        # Step 6a-bis: Literacy growth
        # Uses security (just computed), wealth output, and policy state.
        # Pop growth rate from previous turn is passed as 0.0 if unavailable
        # (first turn or not yet computed); dilution is a secondary effect.
        wealth_per_cap = raw_production.get("wealth", 0.0) / max(province.population, 1)
        province.literacy = compute_literacy_growth(
            province=province,
            bldg_effects=bldg_effects,
            security=province.local_security,
            wealth_per_cap=wealth_per_cap,
            pop_growth_rate=0.0,  # previous turn's rate — computed at Step 13
            active_policies=active_policies,
            trait_effects=trait_effects,
        )

        # Step 6b: Province happiness (static recompute, same as security)
        # Literacy amplifies the trait-policy alignment delta.
        province.local_happiness = compute_province_happiness(
            province=province,
            nation=nation,
            trait_effects=trait_effects,
            active_policies=active_policies,
            literacy=province.literacy,
        )
        # Libertarian control bonus: low control → more happiness and stability recovery.
        if is_libertarian:
            lib_stab_bonus, lib_hap_bonus = compute_libertarian_control_bonus(
                province_control, is_strong=is_libertarian_strong
            )
            province.local_happiness = min(100.0, province.local_happiness + lib_hap_bonus)
        else:
            lib_stab_bonus = 0.0
        happiness_recovery_mult = get_happiness_stability_recovery_multiplier(province.local_happiness)

        # Step 6b-bis: Normalization penalties for non-core provinces.
        # Check if normalization has completed first (promotes to core).
        # If still normalizing, apply happiness and stability penalties that
        # decrease linearly as the province integrates.
        normalization_stability_penalty = 0.0
        if not province.is_core:
            just_completed = check_normalization_completion(province, nation, turn_number)
            if not just_completed:
                norm_stab_pen, norm_hap_pen = compute_normalization_penalties(
                    province, nation, turn_number
                )
                province.local_happiness = max(0.0, province.local_happiness - norm_hap_pen)
                normalization_stability_penalty = norm_stab_pen

        effective_recovery = (
            (STABILITY_RECOVERY_RATE + bldg_effects.get("stability_recovery_bonus", 0.0) + lib_stab_bonus)
            * security_stability_mult
            * happiness_recovery_mult
        )
        if effective_food < local_food_consumption:
            province.local_stability = max(
                0, province.local_stability - STABILITY_FOOD_DEFICIT_PENALTY - normalization_stability_penalty
            )
        else:
            province.local_stability = min(
                100, province.local_stability + effective_recovery - normalization_stability_penalty
            )

        # Store growth_bonus and happiness for use in Step 13
        province_job_status[province.id]["growth_bonus"] = bldg_effects.get("growth_bonus", 0.0)
        province_job_status[province.id]["local_happiness"] = province.local_happiness

        # ----------------------------------------------------------------
        # Step 7: Persist province state
        # ----------------------------------------------------------------
        resources_obj, _ = ProvinceResources.objects.get_or_create(province=province)
        for key in RESOURCE_KEYS:
            setattr(resources_obj, key, raw_production[key])
        resources_obj.updated_turn = turn_number
        resources_obj.save()

        province.designation = designation
        province.save(update_fields=[
            "local_stability", "local_security", "local_happiness", "literacy", "designation",
            "ideology_traits", "is_core", "normalization_started_turn", "normalization_duration",
            "control", "is_rebel_occupied", "rebel_timer_start_turn", "rebel_timer_duration",
        ])

        ProvinceLedger.objects.create(
            province=province,
            turn_number=turn_number,
            population=province.population,
            sector_allocations=job_status,  # repurposed field: stores job snapshot
            raw_production=raw_production,
            local_consumption=local_consumption,
            exported_to_nation=exported,
        )

        # Accumulate national totals
        for key in RESOURCE_KEYS:
            total_province_production[key] += raw_production[key]
            total_local_consumption[key] += local_consumption.get(key, 0)
            total_exported[key] += exported[key]
            if exported[key] < raw_production[key] - local_consumption.get(key, 0):
                total_integration_losses[key] += round(
                    (raw_production[key] - local_consumption.get(key, 0)) - exported[key], 2
                )

    # Step 7: Apply national production modifiers (includes trait bonuses)
    national_modifier_effects = empty_resources()
    production_modifiers = dict(national_modifiers.get("production", {}))
    # Merge trait production bonuses into production modifiers
    if wealth_mod_from_traits:
        production_modifiers["wealth"] = production_modifiers.get("wealth", 0) + wealth_mod_from_traits
    modified_pool = {}
    for key in RESOURCE_KEYS:
        mod = production_modifiers.get(key, 0)
        effect = round(total_exported[key] * mod, 2)
        national_modifier_effects[key] = effect
        modified_pool[key] = round(total_exported[key] + effect, 2)

    # Step 7b: Apply literacy multiplier to national research production.
    # National literacy (mean of province values) gates how much research
    # the nation effectively accumulates. At 20% literacy: 0.5×; at 100%: 1.3×.
    national_literacy = get_national_literacy(provinces)
    literacy_research_mult = get_literacy_research_multiplier(national_literacy)
    modified_pool["research"] = round(modified_pool["research"] * literacy_research_mult, 2)

    # Step 8: Trade imports — deliver in-flight goods that have arrived this turn.
    # Imported goods are available for current-turn pool calculations below.
    from trade.simulation import process_trade_imports
    from .models import NationGoodStock
    good_stock_import, _ = NationGoodStock.objects.get_or_create(nation=nation)
    import_net = process_trade_imports(nation, turn_number, pool, good_stock_import)
    trade_net = empty_resources()
    for good, amount in import_net.items():
        if good in trade_net:
            trade_net[good] = round(trade_net[good] + amount, 4)

    # Step 9: Government upkeep
    # upkeep_reduction from buildings (e.g. banks, fuel depots) and traits reduces total upkeep.
    consumption_modifier = national_modifiers.get("consumption", 0)
    gov_upkeep = empty_resources()
    base_upkeep_wealth = total_pop * 0.01
    total_upkeep_reduction = min(0.75, upkeep_reduction + upkeep_reduction_from_traits)
    upkeep_scale = (1 + consumption_modifier) * (1.0 - total_upkeep_reduction)
    gov_upkeep["wealth"] = round(base_upkeep_wealth * upkeep_scale, 2)
    gov_upkeep["energy"] = round(total_pop * 0.005 * upkeep_scale, 2)

    # Step 10: Final pool calculation
    final_pools = empty_resources()
    for key in RESOURCE_KEYS:
        final = pool.__dict__.get(key, 0) + modified_pool.get(key, 0) + trade_net[key] - gov_upkeep.get(key, 0)
        final_pools[key] = round(max(0, final), 2)

    # Step 11: National stability (includes trait bonuses + bureaucratic deficit)
    stability_modifier = national_modifiers.get("stability", 0) + stability_bonus_from_traits
    avg_stability = sum(p.local_stability for p in provinces) / len(provinces) if provinces else 50
    national_stability = max(0, min(100, avg_stability + stability_modifier - bc_stability_penalty))
    final_pools["stability"] = round(national_stability, 2)

    # Step 11.5: Control-ideology national effects + rebellion tick.
    # Authoritarian nations suffer happiness penalty from low-control provinces.
    # Egalitarian nations gain happiness bonus when control is uniform.
    # Both applied to the national happiness (not per-province).
    national_happiness = (
        sum(p.local_happiness for p in provinces) / len(provinces) if provinces else 50.0
    )
    if is_authoritarian and province_controls:
        auth_penalty = compute_authoritarian_national_penalty(
            province_controls, is_strong=is_authoritarian_strong
        )
        national_happiness = max(0.0, national_happiness - auth_penalty)
    if is_egalitarian and province_controls:
        egal_bonus = compute_egalitarian_national_bonus(
            province_controls, is_strong=is_egalitarian_strong
        )
        national_happiness = min(100.0, national_happiness + egal_bonus)

    # Run rebellion tick: trigger new rebellions, check suppression, resolve timers.
    from .rebellion import process_rebellion_tick
    process_rebellion_tick(provinces, nation, turn_number)

    # Step 12: Food deficit collapse tracking
    if final_pools["food"] <= 0:
        pool.consecutive_food_deficit_turns += 1
    else:
        pool.consecutive_food_deficit_turns = 0

    # Step 13: Population growth — per province (food + stockpile + stability)
    province_growth_rates = {}
    total_pop_after = 0
    for province in provinces:
        food_produced, food_needed = province_food[province.id]
        # Merge building growth_bonus and trait growth into modifiers for this province.
        bldg_growth = province_job_status.get(province.id, {}).get("growth_bonus", 0.0)
        security_growth = get_security_growth_bonus(province.local_security)
        province_modifiers = dict(national_modifiers)
        province_modifiers["growth"] = (
            national_modifiers.get("growth", 0.0) + bldg_growth + growth_bonus_from_traits + security_growth
        )

        # Trait: urban growth penalty (ecologist)
        prov_designation = getattr(province, "designation", "rural")
        urban_growth_penalty = trait_effects.get("urban_growth_penalty", 0.0)
        if prov_designation == "urban" and urban_growth_penalty:
            province_modifiers["growth"] += urban_growth_penalty
        growth_rate = calculate_province_growth_rate(
            food_produced=food_produced,
            food_needed=food_needed,
            national_stockpile=final_pools["food"],
            total_pop=total_pop,
            national_stability=final_pools["stability"],
            modifiers=province_modifiers,
        )
        prov_happiness = province_job_status.get(province.id, {}).get("local_happiness", 50.0)
        growth_rate *= get_happiness_growth_multiplier(prov_happiness)
        province_growth_rates[province.id] = growth_rate
        province.population = max(100, int(province.population * (1 + growth_rate)))
        province.save(update_fields=["population"])
        total_pop_after += province.population

    # Step 13b: Starvation migration — people flee declining provinces.
    # Nation-wide decline → external emigration (national total decreases).
    starvation_immigration = simulate_migration(provinces, province_growth_rates)

    # Step 13c: Economic migration — subsistence workers move toward unfilled jobs.
    # Always internal; national total is conserved.
    economic_immigration = simulate_economic_migration(provinces, province_growth_rates, province_job_status)

    # Step 13d: Apply immigration security penalty.
    # Provinces that received migrants this turn get a security hit unless the
    # nation has the Internationalist trait (strong or weak).
    if not has_internationalist:
        combined_immigration = dict(starvation_immigration)
        for pid, count in economic_immigration.items():
            combined_immigration[pid] = combined_immigration.get(pid, 0) + count
        provinces_by_id = {p.id: p for p in provinces}
        for province_id, migrants_in in combined_immigration.items():
            province = provinces_by_id.get(province_id)
            if province is None or province.population <= 0:
                continue
            immigration_pct = migrants_in / province.population
            if immigration_pct > 0.0:
                from economy.security_constants import (
                    SECURITY_IMMIGRATION_PENALTY_RATE,
                    SECURITY_IMMIGRATION_PENALTY_CAP,
                )
                penalty = max(
                    SECURITY_IMMIGRATION_PENALTY_CAP,
                    immigration_pct * 100.0 * SECURITY_IMMIGRATION_PENALTY_RATE,
                )
                province.local_security = max(0.0, min(100.0, province.local_security + penalty))
                province.save(update_fields=["local_security"])

    # Recalculate after all migration (starvation migration may reduce national total)
    total_pop_after = sum(p.population for p in provinces)

    # Step 14: Advance construction timers
    # Pass Militarist training_speed_bonus so unit training benefits from the trait.
    training_speed_bonus = trait_effects.get("training_speed_bonus", 0.0)
    for province in provinces:
        process_construction_tick(province, training_speed_bonus=training_speed_bonus)

    # Persist national pool
    for key in RESOURCE_KEYS:
        setattr(pool, key, final_pools[key])
    pool.stability = final_pools.get("stability", 50)
    pool.happiness = round(national_happiness, 2)
    pool.literacy = round(national_literacy, 4)
    pool.total_population = total_pop_after
    pool.save()

    # Resource ledger
    ResourceLedger.objects.create(
        nation=nation,
        turn_number=turn_number,
        province_production_total={k: round(v, 2) for k, v in total_province_production.items()},
        integration_losses={k: round(v, 2) for k, v in total_integration_losses.items()},
        national_modifier_effects={k: round(v, 2) for k, v in national_modifier_effects.items()},
        trade_net=trade_net,
        consumption={k: round(v, 2) for k, v in gov_upkeep.items()},
        final_pools=final_pools,
    )

    # Step 15: Building production (workers → manufactured goods)
    # Gather multi-source efficiency modifiers once per nation per turn.
    bldg_eff_mods = get_building_efficiency_modifiers(nation, turn_number)
    rationing_level = _get_rationing_level(nation)
    unit_upkeep_needs = _compute_unit_needs(nation, trait_effects)
    simulate_building_production(
        nation, provinces, province_job_status, bldg_eff_mods,
        rationing_level=rationing_level,
        unit_needs=unit_upkeep_needs,
        worker_productivity=worker_productivity,
        province_dp_multipliers=province_dp_multipliers,
    )

    # Step 16: Consumer goods consumption (shortage → stability penalty)
    simulate_good_consumption(nation, total_pop_after)

    # Step 16.5: Trade exports — deduct from post-spend stocks and push to in_flight.
    # Exports use whatever remains after domestic consumption; shortfall is capped
    # (partial shipment) and does not trigger shortages for the rest of the economy.
    from trade.simulation import process_trade_exports
    from .models import NationGoodStock
    good_stock_export, _ = NationGoodStock.objects.get_or_create(nation=nation)
    export_net = process_trade_exports(nation, turn_number, pool, good_stock_export)
    for good, amount in export_net.items():
        if good in trade_net:
            trade_net[good] = round(trade_net[good] + amount, 4)  # amount is negative

    # Step 17: Military upkeep deduction
    # Returns (manpower_supply_ratio, food_supply_ratio) used in Step 18.
    manpower_ratio, food_ratio = _apply_military_upkeep(nation, provinces, trait_effects)

    # Step 18: Formation effective_strength recompute
    _update_formation_strengths(nation, manpower_ratio, food_ratio)

    # Step 18.5: ControlPoolSnapshot — informational record of retained vs. national flow.
    _persist_control_pool_snapshots(provinces, nation, turn_number, integration_modifier)

    # Step 19: Annual DP grant (System 17)
    _grant_annual_dp(nation, turn_number)


def _persist_control_pool_snapshots(provinces, nation, turn_number: int, integration_modifier: float) -> None:
    """Persist per-turn ControlPoolSnapshot rows for provinces and regions.

    For each province not in a region, creates one snapshot recording what the
    control level retained locally vs. what flowed to the national government.
    Provinces in a region are aggregated into a single snapshot per region.

    The snapshot is informational only and does not affect gameplay.
    """
    from .models import ControlPoolSnapshot
    from provinces.models import ProvinceResources

    region_data = {}   # region_id → aggregated totals
    province_rows = []

    for province in provinces:
        control = get_province_control(province)
        flow = compute_national_flow_fraction(control)
        retain = 1.0 - flow

        # Pull raw production from ProvinceResources (just saved this turn).
        try:
            res = ProvinceResources.objects.get(province=province)
            prov_integration = min(1.0, integration_modifier)
            # Total = surplus that would flow under full integration + control.
            # Approximate using manpower as 0 (not a "taxable" resource).
            tax_total = round((res.wealth or 0.0) * prov_integration, 2)
            trade_total = round(((res.materials or 0.0) + (res.energy or 0.0)) * prov_integration, 2)
            bc_total = round((res.research or 0.0) * prov_integration, 2)
            research_total = bc_total
        except Exception:
            tax_total = trade_total = bc_total = research_total = 0.0

        if province.region_id is None:
            province_rows.append(ControlPoolSnapshot(
                province=province,
                region=None,
                turn_number=turn_number,
                tax_revenue_total=tax_total,
                tax_revenue_retained=round(tax_total * retain, 2),
                trade_capacity_total=trade_total,
                trade_capacity_retained=round(trade_total * retain, 2),
                bc_total=bc_total,
                bc_retained=round(bc_total * retain, 2),
                research_total=research_total,
                research_retained=round(research_total * retain, 2),
            ))
        else:
            r = province.region_id
            if r not in region_data:
                region_data[r] = {
                    "region_id": r,
                    "control": control,
                    "tax": 0.0, "trade": 0.0, "bc": 0.0, "research": 0.0,
                }
            region_data[r]["tax"] += tax_total
            region_data[r]["trade"] += trade_total
            region_data[r]["bc"] += bc_total
            region_data[r]["research"] += research_total

    region_rows = []
    for r_id, totals in region_data.items():
        control = totals["control"]
        retain = 1.0 - compute_national_flow_fraction(control)
        region_rows.append(ControlPoolSnapshot(
            province=None,
            region_id=r_id,
            turn_number=turn_number,
            tax_revenue_total=round(totals["tax"], 2),
            tax_revenue_retained=round(totals["tax"] * retain, 2),
            trade_capacity_total=round(totals["trade"], 2),
            trade_capacity_retained=round(totals["trade"] * retain, 2),
            bc_total=round(totals["bc"], 2),
            bc_retained=round(totals["bc"] * retain, 2),
            research_total=round(totals["research"], 2),
            research_retained=round(totals["research"] * retain, 2),
        ))

    ControlPoolSnapshot.objects.bulk_create(province_rows + region_rows)


def _grant_annual_dp(nation, current_turn):
    """Grant DP_ANNUAL_GRANT points every DP_GRANT_INTERVAL turns."""
    from nations.models import NationDPPool
    from .dp_constants import DP_ANNUAL_GRANT, DP_GRANT_INTERVAL

    if current_turn < 1 or current_turn % DP_GRANT_INTERVAL != 0:
        return

    pool, _ = NationDPPool.objects.get_or_create(
        nation=nation, defaults={"available_points": 0, "last_grant_turn": 0}
    )
    pool.available_points += DP_ANNUAL_GRANT
    pool.last_grant_turn = current_turn
    pool.save(update_fields=["available_points", "last_grant_turn"])


def _apply_military_upkeep(nation, provinces, trait_effects):
    """
    Deduct per-unit-per-turn upkeep costs from the nation's resource pools.

    Basic resources (food, manpower, wealth, energy) are deducted from
    NationResourcePool; manufactured goods (military_goods, fuel) are deducted
    from NationGoodStock.  Units whose manufactured-goods or fuel upkeep cannot
    be met are set to is_active=False (they are NOT destroyed).

    Manpower and food deficits reduce effective_strength (handled in
    _update_formation_strengths) but do NOT deactivate units — the unit still
    exists, it just operates at reduced combat effectiveness.

    Returns
    -------
    (manpower_supply_ratio, food_supply_ratio) : tuple[float, float]
        Fractions of manpower/food upkeep that were available (capped at 1.0).
        Used by _update_formation_strengths to compute effective_strength.
    """
    from provinces.military_constants import UNIT_TYPES
    from provinces.models import MilitaryUnit
    from .models import NationGoodStock, NationResourcePool
    from economy.building_simulation import _POOL_RESOURCE_KEYS

    upkeep_reduction = min(0.75, trait_effects.get("military_upkeep_reduction", 0.0))

    pool = NationResourcePool.objects.get(nation=nation)
    good_stock, _ = NationGoodStock.objects.get_or_create(nation=nation)

    # Gather all active units across provinces
    province_ids = [p.id for p in provinces]
    active_units = list(
        MilitaryUnit.objects.filter(
            formation__nation=nation,
            quantity__gt=0,
        ).select_related("formation")
    )

    if not active_units:
        return 1.0, 1.0

    # --- First pass: compute total manpower and food needed ---
    total_manpower_needed = 0.0
    total_food_needed = 0.0
    for unit in active_units:
        unit_def = UNIT_TYPES.get(unit.unit_type, {})
        upkeep = unit_def.get("upkeep", {})
        scale = unit.quantity * (1.0 - upkeep_reduction)
        total_manpower_needed += upkeep.get("manpower", 0.0) * scale
        total_food_needed += upkeep.get("food", 0.0) * scale

    manpower_supply_ratio = (
        min(1.0, pool.manpower / total_manpower_needed)
        if total_manpower_needed > 0 else 1.0
    )
    food_supply_ratio = (
        min(1.0, pool.food / total_food_needed)
        if total_food_needed > 0 else 1.0
    )

    # Deduct manpower and food (clamp to 0, do not deactivate)
    pool.manpower = round(max(0.0, pool.manpower - total_manpower_needed), 4)
    pool.food = round(max(0.0, pool.food - total_food_needed), 4)

    # --- Second pass: deduct manufactured goods and other pool costs per unit ---
    pool_dirty = True  # manpower/food were already modified
    stock_dirty = False

    for unit in active_units:
        unit_def = UNIT_TYPES.get(unit.unit_type, {})
        upkeep = unit_def.get("upkeep", {})
        unit_is_active = True

        for good, amount_per_unit in upkeep.items():
            if good in ("manpower", "food"):
                continue  # handled above
            total = round(amount_per_unit * unit.quantity * (1.0 - upkeep_reduction), 4)
            if good in _POOL_RESOURCE_KEYS:
                current = getattr(pool, good, 0.0)
                setattr(pool, good, round(max(0.0, current - total), 4))
            else:
                current = getattr(good_stock, good, 0.0)
                if current < total:
                    unit_is_active = False
                else:
                    setattr(good_stock, good, round(current - total, 4))
                    stock_dirty = True

        if unit.is_active != unit_is_active:
            unit.is_active = unit_is_active
            unit.save(update_fields=["is_active"])

    pool.save()
    if stock_dirty:
        good_stock.save()

    return manpower_supply_ratio, food_supply_ratio


def _update_formation_strengths(nation, manpower_ratio, food_ratio):
    """
    Recompute and persist effective_strength for every Formation in the nation.

    effective_strength = sum(active unit quantities) × manpower_ratio × food_ratio

    The formula can yield values above sum(quantity) when morale/trait bonuses
    are added in future systems (manpower_ratio and food_ratio are currently
    capped at 1.0, but this function is the right place to add multipliers).

    Called at the end of each turn simulation after military upkeep is resolved.
    """
    from provinces.models import Formation

    formations = (
        Formation.objects
        .filter(nation=nation)
        .prefetch_related("units")
    )
    for formation in formations:
        total_quantity = sum(
            u.quantity for u in formation.units.all()
            if u.is_active and u.quantity > 0
        )
        formation.effective_strength = round(
            total_quantity * manpower_ratio * food_ratio, 4
        )
        formation.save(update_fields=["effective_strength"])


def _gather_national_modifiers(nation, turn_number):
    """Collect all active national modifiers into a structured dict."""
    result = {"production": {}, "integration": 0, "stability": 0, "growth": 0,
              "consumption": 0, "trade": 0, "military": 0, "research": 0}

    for mod in nation.modifiers.all():
        if mod.expires_turn and mod.expires_turn < turn_number:
            continue

        if mod.category == "economy" and mod.target in RESOURCE_KEYS:
            result["production"][mod.target] = result["production"].get(mod.target, 0) + mod.value
        elif mod.target in result:
            if isinstance(result[mod.target], dict):
                continue
            result[mod.target] += mod.value

    return result
