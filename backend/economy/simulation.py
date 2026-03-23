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

    nations = Nation.objects.filter(game=game, is_alive=True).prefetch_related(
        "provinces__buildings",
        "provinces__resources",
        "modifiers",
    )

    for nation in nations:
        simulate_nation_economy(nation, turn_number)


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

    # Apply trait + policy bonuses to national modifiers
    integration_bonus_from_traits = (
        trait_effects.get("integration_bonus", 0.0)
        + policy_effects.get("integration_bonus", 0.0)
    )
    stability_bonus_from_traits = (
        trait_effects.get("stability_bonus", 0.0) + trait_effects.get("stability_penalty", 0.0)
        + policy_effects.get("stability_bonus", 0.0) + policy_effects.get("stability_penalty", 0.0)
    )
    growth_bonus_from_traits = (
        trait_effects.get("growth_bonus", 0.0) + trait_effects.get("growth_penalty", 0.0)
        + policy_effects.get("growth_bonus", 0.0) + policy_effects.get("growth_penalty", 0.0)
    )
    research_mod_from_traits = (
        trait_effects.get("research_bonus", 0.0) + trait_effects.get("research_penalty", 0.0)
        + policy_effects.get("research_bonus", 0.0) + policy_effects.get("research_penalty", 0.0)
    )
    manpower_mod_from_traits = (
        trait_effects.get("manpower_bonus", 0.0)
        + policy_effects.get("manpower_bonus", 0.0)
    )
    wealth_mod_from_traits = (
        trait_effects.get("wealth_production_bonus", 0.0)
        + policy_effects.get("wealth_production_bonus", 0.0)
    )
    food_mod_from_traits = (
        trait_effects.get("food_production_bonus", 0.0)
        + policy_effects.get("food_production_bonus", 0.0)
    )
    upkeep_reduction_from_traits = (
        trait_effects.get("upkeep_reduction", 0.0)
        + policy_effects.get("upkeep_reduction", 0.0)
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
    province_food = {}       # id → (food_produced, food_needed)
    province_job_status = {} # id → job status dict

    # National building effects (upkeep_reduction, construction_cost_reduction)
    national_bldg_effects = get_national_building_effects(provinces)
    upkeep_reduction = min(0.75, national_bldg_effects.get("upkeep_reduction", 0.0))

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

        raw_production["manpower"] = round(
            province.population * MANPOWER_PER_POP * desg_mods.get("manpower", 1.0)
            * (1.0 + manpower_mod_from_traits),
            2,
        )

        # ----------------------------------------------------------------
        # Step 4: Local consumption (food for population)
        # ----------------------------------------------------------------
        local_food_consumption = province.population * FOOD_CONSUMPTION_PER_POP
        local_consumption = empty_resources()
        local_consumption["food"] = round(local_food_consumption, 2)

        # ----------------------------------------------------------------
        # Step 5: Province surplus → exported to nation (with integration)
        #   integration_bonus from buildings adds to per-province integration.
        # ----------------------------------------------------------------
        province_integration = min(1.0, integration_modifier + bldg_effects.get("integration_bonus", 0.0))
        exported = empty_resources()
        for key in RESOURCE_KEYS:
            surplus = raw_production[key] - local_consumption.get(key, 0)
            if surplus > 0:
                exported[key] = round(surplus * province_integration, 2)
            else:
                exported[key] = round(surplus, 2)  # deficit passes through fully

        # Store food data for growth calculation (after final pool is known)
        province_food[province.id] = (raw_production["food"], local_consumption["food"])

        # ----------------------------------------------------------------
        # Step 6: Province stability — considers national food supplement
        #   Uses previous turn's pool.food so non-food provinces aren't
        #   perpetually penalised when the nation has a healthy stockpile.
        #   stability_recovery_bonus from buildings adds to recovery rate.
        # ----------------------------------------------------------------
        effective_recovery = STABILITY_RECOVERY_RATE + bldg_effects.get("stability_recovery_bonus", 0.0)
        national_food_share = (pool.food / max(total_pop, 1)) * province.population
        effective_food = raw_production["food"] + national_food_share
        if effective_food < local_food_consumption:
            province.local_stability = max(0, province.local_stability - STABILITY_FOOD_DEFICIT_PENALTY)
        else:
            province.local_stability = min(100, province.local_stability + effective_recovery)

        # Store growth_bonus for use in Step 13
        province_job_status[province.id]["growth_bonus"] = bldg_effects.get("growth_bonus", 0.0)

        # ----------------------------------------------------------------
        # Step 7: Persist province state
        # ----------------------------------------------------------------
        resources_obj, _ = ProvinceResources.objects.get_or_create(province=province)
        for key in RESOURCE_KEYS:
            setattr(resources_obj, key, raw_production[key])
        resources_obj.updated_turn = turn_number
        resources_obj.save()

        province.designation = designation
        province.save(update_fields=["local_stability", "designation"])

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

    # Step 8: Trade execution (placeholder)
    trade_net = empty_resources()

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

    # Step 11: National stability (includes trait bonuses)
    stability_modifier = national_modifiers.get("stability", 0) + stability_bonus_from_traits
    avg_stability = sum(p.local_stability for p in provinces) / len(provinces) if provinces else 50
    national_stability = max(0, min(100, avg_stability + stability_modifier))
    final_pools["stability"] = round(national_stability, 2)

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
        province_modifiers = dict(national_modifiers)
        province_modifiers["growth"] = national_modifiers.get("growth", 0.0) + bldg_growth + growth_bonus_from_traits

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
        province_growth_rates[province.id] = growth_rate
        province.population = max(100, int(province.population * (1 + growth_rate)))
        province.save(update_fields=["population"])
        total_pop_after += province.population

    # Step 13b: Starvation migration — people flee declining provinces.
    # Nation-wide decline → external emigration (national total decreases).
    simulate_migration(provinces, province_growth_rates)

    # Step 13c: Economic migration — subsistence workers move toward unfilled jobs.
    # Always internal; national total is conserved.
    simulate_economic_migration(provinces, province_growth_rates, province_job_status)

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
    )

    # Step 16: Consumer goods consumption (shortage → stability penalty)
    simulate_good_consumption(nation, total_pop_after)

    # Step 17: Military upkeep deduction
    # Returns (manpower_supply_ratio, food_supply_ratio) used in Step 18.
    manpower_ratio, food_ratio = _apply_military_upkeep(nation, provinces, trait_effects)

    # Step 18: Formation effective_strength recompute
    _update_formation_strengths(nation, manpower_ratio, food_ratio)


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
