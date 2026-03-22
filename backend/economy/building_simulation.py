"""
Building production simulation.

Handles manufactured goods production/consumption each turn, building effect
helpers, and the multi-source building efficiency modifier system.

Building output each turn
=========================
  output = amount × effective_capacity × designation_mult × efficiency_mult

effective_capacity = min(worker_capacity_factor, input_goods_capacity)
designation_mult   = DESIGNATION_BUILDING_MODIFIER[province.designation]
efficiency_mult    = 1.0 + sum(all efficiency bonuses below)

Efficiency modifier sources (each is separately additive)
----------------------------------------------------------
1. Government type  — GOVERNMENT_TYPES[gov]["building_efficiency"][category]
2. Trait bonuses    — building_efficiency_bonus from ideology traits
3. GM crisis/boon   — NationModifier(category="building_efficiency", target=category_or_"all")
4. Input co-location— province terrain primary resource is in building's input_goods (+INPUT_COLOCATION_BONUS)
5. Concentration    — SAME_TYPE × building.level  +  SAME_CATEGORY × other_category_levels
                      (replaces old per-building INDUSTRY_CLUSTER_BONUS)

Sources 1-3 are national (same for all buildings of a given category).
Sources 4-5 are per-building/per-province.

Buildings have unlimited levels. All level-specific data is obtained via
get_level_data(building_type, level) from provinces.building_constants.
"""

# Basic resource keys stored in NationResourcePool
_POOL_RESOURCE_KEYS = ["food", "materials", "energy", "wealth", "manpower", "research"]

from provinces.constants import DESIGNATION_BUILDING_MODIFIER


# ---------------------------------------------------------------------------
# Building effect helpers (used by main simulation loop)
# ---------------------------------------------------------------------------

def get_province_building_effects(province):
    """
    Sum all province-scope effects from active, non-under-construction buildings.

    Uses province.buildings.all() so Django's prefetch_related cache is honoured.

    Returns a dict keyed by PROVINCE_EFFECT_KEYS, values are floats (additive).
    """
    from provinces.building_constants import BUILDING_TYPES, PROVINCE_EFFECT_KEYS, get_level_data

    effects = {k: 0.0 for k in PROVINCE_EFFECT_KEYS}
    for building in province.buildings.all():
        if not building.is_active or building.under_construction:
            continue
        if building.building_type not in BUILDING_TYPES or building.level < 1:
            continue
        level_data = get_level_data(building.building_type, building.level)
        for k, v in level_data["effects"].items():
            if k in effects:
                effects[k] += v
    return effects


def get_national_building_effects(provinces):
    """
    Sum all national-scope effects from active buildings across all provinces.

    Returns a dict keyed by NATIONAL_EFFECT_KEYS, values are floats (additive).
    """
    from provinces.building_constants import BUILDING_TYPES, NATIONAL_EFFECT_KEYS, get_level_data

    effects = {k: 0.0 for k in NATIONAL_EFFECT_KEYS}
    for province in provinces:
        for building in province.buildings.all():
            if not building.is_active or building.under_construction:
                continue
            if building.building_type not in BUILDING_TYPES or building.level < 1:
                continue
            level_data = get_level_data(building.building_type, building.level)
            for k, v in level_data["effects"].items():
                if k in effects:
                    effects[k] += v
    return effects


def get_construction_modifiers(nation):
    """
    Return the national construction_cost_reduction fraction for a nation, clamped to [0, 0.75].
    """
    from provinces.building_constants import BUILDING_TYPES, get_level_data

    cost_reduction = 0.0
    for province in nation.provinces.all():
        for building in province.buildings.all():
            if not building.is_active or building.under_construction:
                continue
            if building.building_type not in BUILDING_TYPES or building.level < 1:
                continue
            level_data = get_level_data(building.building_type, building.level)
            cost_reduction += level_data["effects"].get("construction_cost_reduction", 0.0)

    return min(0.75, cost_reduction)


# ---------------------------------------------------------------------------
# Building efficiency — multi-source modifier system
# ---------------------------------------------------------------------------

def get_building_efficiency_modifiers(nation, turn_number):
    """
    Aggregate national building efficiency modifiers from three sources:

      1. Government type  — GOVERNMENT_TYPES[gov]["building_efficiency"]
      2. Trait bonuses    — building_efficiency_bonus from ideology traits
      3. GM NationModifiers with category="building_efficiency"

    Returns a flat dict mapping building category (or "all") → total bonus float.
    Example: {"heavy_manufacturing": 0.30, "financial": 0.22, "all": -0.15}

    Sources 4 (co-location) and 5 (concentration) are per-province and computed in
    compute_building_efficiency().
    """
    from economy.constants import GOVERNMENT_TYPES
    from nations.helpers import get_nation_trait_effects

    merged = {}

    # Source 1: government type
    gov_def = GOVERNMENT_TYPES.get(nation.government_type, {})
    for cat, bonus in gov_def.get("building_efficiency", {}).items():
        merged[cat] = merged.get(cat, 0.0) + bonus

    # Source 2: trait building_efficiency_bonus
    trait_effects = get_nation_trait_effects(nation)
    for cat, bonus in trait_effects.get("building_efficiency_bonus", {}).items():
        merged[cat] = merged.get(cat, 0.0) + bonus

    # Source 2b: policy building_efficiency_bonus
    from nations.policy_effects import get_nation_policy_effects
    policy_effects = get_nation_policy_effects(nation)
    for cat, bonus in policy_effects.get("building_efficiency_bonus", {}).items():
        merged[cat] = merged.get(cat, 0.0) + bonus

    # Source 3: active GM NationModifiers (crises and boons)
    for mod in nation.modifiers.all():
        if mod.expires_turn and mod.expires_turn < turn_number:
            continue
        if mod.category == "building_efficiency":
            merged[mod.target] = merged.get(mod.target, 0.0) + mod.value

    return merged


def compute_building_efficiency(
    building_type,
    building_level,
    level_data,
    province_terrain,
    province_category_level_sums,
    province_building_outputs,
    building_efficiency_modifiers,
):
    """
    Compute the total efficiency multiplier for a single building instance.

    Parameters
    ----------
    building_type : str
        Key from BUILDING_TYPES.
    building_level : int
        Current level of this specific building instance.
    level_data : dict
        The level config dict from get_level_data() for this building's current level.
    province_terrain : str
        Terrain type of the province (used for co-location check).
    province_category_level_sums : dict[str, int]
        {category: total_level_sum} of ALL active buildings in this province.
        Used for concentration bonus (includes this building's own level).
    province_building_outputs : set[str]
        Set of goods produced by ALL active buildings in this province.
        Used to detect intra-province supply chain co-location.
    building_efficiency_modifiers : dict[str, float]
        National modifiers from get_building_efficiency_modifiers().

    Returns
    -------
    float
        Efficiency multiplier ≥ 0. Values above 1.0 mean above-baseline output.

    Efficiency components (all additive, all separate sources)
    -----------------------------------------------------------
    nat_bonus      : gov + traits + GM modifiers for this building's category
                     plus any "all" modifier
    colocation     : +INPUT_COLOCATION_BONUS if ANY of this building's input goods
                     are produced locally — either by the province terrain's primary
                     resource or by another active building in the same province
    concentration  : SAME_TYPE_CONCENTRATION_BONUS × building_level
                     + SAME_CATEGORY_CONCENTRATION_BONUS × (category_total − building_level)
                     Rewards both deep investment in a single type and broad category clusters.
    """
    from provinces.building_constants import (
        BUILDING_TYPES,
        INPUT_COLOCATION_BONUS,
        SAME_TYPE_CONCENTRATION_BONUS,
        SAME_CATEGORY_CONCENTRATION_BONUS,
    )
    from provinces.jobs import terrain_primary_resource

    b_def = BUILDING_TYPES.get(building_type, {})
    category = b_def.get("category", "")

    # --- Source 1/2/3: national modifier (gov + traits + GM) ---
    nat_bonus = (
        building_efficiency_modifiers.get("all", 0.0)
        + building_efficiency_modifiers.get(category, 0.0)
    )

    # --- Source 4: input co-location ---
    # Fires if ANY input good is available locally, from either:
    #   (a) terrain: the province's primary resource matches an input good, or
    #   (b) supply chain: another active building in the province produces an input good.
    input_keys = set(level_data["input_goods"])
    province_primary = terrain_primary_resource(province_terrain)
    locally_supplied = (province_primary in input_keys) or bool(input_keys & province_building_outputs)
    colocation_bonus = INPUT_COLOCATION_BONUS if locally_supplied else 0.0

    # --- Source 5: concentration bonus ---
    # same_type_score  = this building's level (unique per province, so equals total type sum)
    # same_category_score = total category level sum minus this building's own level
    same_type_score = building_level
    category_total = province_category_level_sums.get(category, 0)
    other_category_score = max(0, category_total - building_level)
    concentration_bonus = (
        SAME_TYPE_CONCENTRATION_BONUS * same_type_score
        + SAME_CATEGORY_CONCENTRATION_BONUS * other_category_score
    )

    return 1.0 + nat_bonus + colocation_bonus + concentration_bonus


# ---------------------------------------------------------------------------
# Rationing — per-sector input-goods capacity allocation
# ---------------------------------------------------------------------------

def compute_rationing_capacities(
    civilian_needs,
    mil_building_needs,
    government_needs,
    unit_needs,
    pool,
    good_stock,
    rationing_level,
):
    """
    Compute per-sector building capacity factors based on the rationing policy.

    The priority sector is served first from the available pool; remaining
    sectors share what is left proportionally.  Within the military sector,
    units are always served before military buildings (under any rationing
    level other than no_rationing).

    Under no_rationing all consumers — buildings and units — compete for the
    same pool on equal terms (a single shared capacity factor).

    Parameters
    ----------
    civilian_needs / mil_building_needs / government_needs : dict[str, float]
        Total input-goods needs (good → amount) for each building sector,
        aggregated with worker_capacity_factor already applied.
    unit_needs : dict[str, float]
        Total upkeep needs (good → amount) for all active military units.
    pool : NationResourcePool
    good_stock : NationGoodStock
    rationing_level : int
        0 = no_rationing, 1 = civilian_priority,
        2 = military_priority, 3 = government_priority

    Returns
    -------
    dict with keys:
        civilian_cap : float          (0.0–1.0)
        military_building_cap : float (0.0–1.0)
        government_cap : float        (0.0–1.0)
        unit_cap : float              (0.0–1.0, informational)
    """
    # Build available-goods snapshot
    available = {g: getattr(pool, g, 0.0) for g in _POOL_RESOURCE_KEYS}
    from provinces.building_constants import GOOD_KEYS
    for g in GOOD_KEYS:
        available[g] = getattr(good_stock, g, 0.0)

    def _cap(needs, avail):
        """Min-ratio capacity factor for a needs dict against an available dict."""
        cap = 1.0
        for g, n in needs.items():
            if n > 0:
                cap = min(cap, avail.get(g, 0.0) / n)
        return max(0.0, cap)

    def _combined(*needs_dicts):
        combined = {}
        for needs in needs_dicts:
            for g, n in needs.items():
                combined[g] = combined.get(g, 0.0) + n
        return combined

    def _deduct(avail, needs, cap):
        remaining = dict(avail)
        for g, n in needs.items():
            remaining[g] = max(0.0, remaining.get(g, 0.0) - n * cap)
        return remaining

    def _proportional_mil_caps(mil_remaining):
        """Given military's allocated goods, compute unit_cap then mil_building_cap."""
        uc = min(1.0, _cap(unit_needs, mil_remaining))
        after_units = _deduct(mil_remaining, unit_needs, uc)
        mbc = min(1.0, _cap(mil_building_needs, after_units))
        return uc, mbc

    def _mil_share(avail):
        """Compute each good's proportional share for the military sector."""
        mil_total = _combined(mil_building_needs, unit_needs)
        sharing = {}
        for g in set(list(mil_total.keys()) + list(avail.keys())):
            mt = mil_total.get(g, 0.0)
            all_sharing = mt + government_needs.get(g, 0.0)
            if all_sharing > 0:
                sharing[g] = avail.get(g, 0.0) * (mt / all_sharing)
            else:
                sharing[g] = 0.0
        return sharing

    if rationing_level == 0:  # no_rationing — single shared cap for all
        total = _combined(civilian_needs, mil_building_needs, government_needs, unit_needs)
        cap = min(1.0, _cap(total, available))
        return {
            "civilian_cap": cap,
            "military_building_cap": cap,
            "government_cap": cap,
            "unit_cap": cap,
        }

    if rationing_level == 1:  # civilian_priority
        civ_cap = min(1.0, _cap(civilian_needs, available))
        remaining = _deduct(available, civilian_needs, civ_cap)

        # Military and government share remainder proportionally
        mil_gov_total = _combined(mil_building_needs, unit_needs, government_needs)
        joint_cap = min(1.0, _cap(mil_gov_total, remaining))

        # Within military's proportional allocation: units first, then buildings
        mil_total = _combined(mil_building_needs, unit_needs)
        mil_alloc = {}
        for g in set(list(mil_total.keys()) + list(remaining.keys())):
            mg = mil_gov_total.get(g, 0.0)
            if mg > 0:
                mil_alloc[g] = remaining.get(g, 0.0) * (mil_total.get(g, 0.0) / mg)
            else:
                mil_alloc[g] = 0.0
        uc, mbc = _proportional_mil_caps(mil_alloc)

        return {
            "civilian_cap": civ_cap,
            "military_building_cap": mbc,
            "government_cap": joint_cap,
            "unit_cap": uc,
        }

    if rationing_level == 2:  # military_priority — units first, then military buildings
        uc = min(1.0, _cap(unit_needs, available))
        after_units = _deduct(available, unit_needs, uc)
        mbc = min(1.0, _cap(mil_building_needs, after_units))
        after_mil = _deduct(after_units, mil_building_needs, mbc)

        # Civilian and government share remainder proportionally
        civ_gov_total = _combined(civilian_needs, government_needs)
        joint_cap = min(1.0, _cap(civ_gov_total, after_mil))

        return {
            "civilian_cap": joint_cap,
            "military_building_cap": mbc,
            "government_cap": joint_cap,
            "unit_cap": uc,
        }

    # rationing_level == 3 — government_priority
    gov_cap = min(1.0, _cap(government_needs, available))
    remaining = _deduct(available, government_needs, gov_cap)

    # Civilian and military (units then buildings) share remainder proportionally
    mil_total = _combined(mil_building_needs, unit_needs)
    civ_mil_total = _combined(civilian_needs, mil_total)
    joint_cap = min(1.0, _cap(civ_mil_total, remaining))

    mil_alloc = {}
    for g in set(list(mil_total.keys()) + list(remaining.keys())):
        cm = civ_mil_total.get(g, 0.0)
        if cm > 0:
            mil_alloc[g] = remaining.get(g, 0.0) * (mil_total.get(g, 0.0) / cm)
        else:
            mil_alloc[g] = 0.0
    uc, mbc = _proportional_mil_caps(mil_alloc)

    return {
        "civilian_cap": joint_cap,
        "military_building_cap": mbc,
        "government_cap": gov_cap,
        "unit_cap": uc,
    }


# ---------------------------------------------------------------------------
# Main production functions
# ---------------------------------------------------------------------------

def simulate_building_production(
    nation, provinces, province_job_status, building_efficiency_modifiers,
    rationing_level=0, unit_needs=None,
):
    """
    Process manufactured-goods production for all buildings in a nation.

    Capacity is the stricter of two independent limits:
      - Worker capacity   (per province): filled_jobs / job_capacity
      - Input goods capacity (national):  min(available[good] / needed[good])

    Efficiency multiplier is applied to outputs only (not inputs) and combines:
      - Designation multiplier (urban provinces produce more)
      - Multi-source efficiency from get_building_efficiency_modifiers() +
        compute_building_efficiency() (gov/traits/GM/colocation/concentration)

    Input goods are split between NationResourcePool (basic resources) and
    NationGoodStock (manufactured goods).  Output goods are routed to whichever
    store owns that field.

    Parameters
    ----------
    building_efficiency_modifiers : dict
        Pre-computed national efficiency modifiers from get_building_efficiency_modifiers().
        Pass an empty dict if callers do not need the modifier system.
    rationing_level : int
        0 = no_rationing (default), 1 = civilian_priority,
        2 = military_priority, 3 = government_priority.
    unit_needs : dict[str, float] or None
        Total upkeep needs of all active military units this turn
        (good → amount, with upkeep_reduction already applied).
        Pass None or {} if there are no units or rationing is unused.
    """
    from provinces.building_constants import BUILDING_TYPES, BUILDING_SECTOR, get_level_data
    from .models import NationGoodStock, NationResourcePool

    pool = NationResourcePool.objects.get(nation=nation)
    good_stock, _ = NationGoodStock.objects.get_or_create(nation=nation)

    if unit_needs is None:
        unit_needs = {}

    # ------------------------------------------------------------------
    # Pre-compute per-province snapshots for efficiency bonuses.
    # Both use province.buildings.all() so the prefetch cache is hit.
    # province_category_level_sums: province.id → {category: total level sum}
    # province_building_outputs:    province.id → set of goods produced
    # ------------------------------------------------------------------
    province_category_level_sums = {}
    province_building_outputs = {}
    for province in provinces:
        level_sums = {}
        outputs = set()
        for building in province.buildings.all():
            if not building.is_active or building.under_construction:
                continue
            if building.building_type not in BUILDING_TYPES or building.level < 1:
                continue
            b_def = BUILDING_TYPES[building.building_type]
            cat = b_def.get("category", "")
            if cat:
                level_sums[cat] = level_sums.get(cat, 0) + building.level
            lvl_data = get_level_data(building.building_type, building.level)
            outputs.update(lvl_data["output_goods"])
        province_category_level_sums[province.id] = level_sums
        province_building_outputs[province.id] = outputs

    # ------------------------------------------------------------------
    # Collect active buildings, split input needs by sector.
    # Tuple: (building, level_data, worker_capacity_factor, designation,
    #         province_terrain, province_id, sector)
    # ------------------------------------------------------------------
    active_buildings = []
    sector_needed = {"civilian": {}, "military": {}, "government": {}}

    for province in provinces:
        wf = province_job_status.get(province.id, {}).get("worker_capacity_factor", 1.0)
        for building in province.buildings.all():
            if not building.is_active or building.under_construction:
                continue
            if building.building_type not in BUILDING_TYPES or building.level < 1:
                continue
            level_data = get_level_data(building.building_type, building.level)
            designation = getattr(province, "designation", "rural")
            sector = BUILDING_SECTOR.get(building.building_type, "civilian")
            active_buildings.append((
                building, level_data, wf, designation,
                province.terrain_type, province.id, sector,
            ))
            s_needs = sector_needed[sector]
            for good, amount in level_data["input_goods"].items():
                s_needs[good] = s_needs.get(good, 0) + amount * wf

    if not active_buildings:
        return

    # ------------------------------------------------------------------
    # Compute per-sector capacity factors via rationing policy.
    # ------------------------------------------------------------------
    rationing_caps = compute_rationing_capacities(
        civilian_needs=sector_needed["civilian"],
        mil_building_needs=sector_needed["military"],
        government_needs=sector_needed["government"],
        unit_needs=unit_needs,
        pool=pool,
        good_stock=good_stock,
        rationing_level=rationing_level,
    )

    # ------------------------------------------------------------------
    # Process each building.
    # output = amount × effective_capacity × designation_mult × efficiency_mult
    # ------------------------------------------------------------------
    pool_dirty = False
    stock_dirty = False

    _sector_cap_key = {
        "civilian":   "civilian_cap",
        "military":   "military_building_cap",
        "government": "government_cap",
    }

    for bldg, level_data, wf, designation, province_terrain, province_id, sector in active_buildings:
        sector_cap = rationing_caps[_sector_cap_key[sector]]
        effective_capacity = min(sector_cap, wf)
        designation_mult = DESIGNATION_BUILDING_MODIFIER.get(designation, 1.0)
        efficiency_mult = compute_building_efficiency(
            bldg.building_type,
            bldg.level,
            level_data,
            province_terrain,
            province_category_level_sums.get(province_id, {}),
            province_building_outputs.get(province_id, set()),
            building_efficiency_modifiers,
        )

        for good, amount in level_data["input_goods"].items():
            deduct = round(amount * effective_capacity, 4)
            if good in _POOL_RESOURCE_KEYS:
                setattr(pool, good, max(0.0, getattr(pool, good, 0.0) - deduct))
                pool_dirty = True
            else:
                setattr(good_stock, good, max(0.0, getattr(good_stock, good, 0.0) - deduct))
                stock_dirty = True

        for good, amount in level_data["output_goods"].items():
            produce = round(amount * effective_capacity * designation_mult * efficiency_mult, 4)
            if good in _POOL_RESOURCE_KEYS:
                setattr(pool, good, round(getattr(pool, good, 0.0) + produce, 4))
                pool_dirty = True
            else:
                setattr(good_stock, good, round(getattr(good_stock, good, 0.0) + produce, 4))
                stock_dirty = True

    if pool_dirty:
        pool.save(update_fields=_POOL_RESOURCE_KEYS)
    if stock_dirty:
        good_stock.save()


def simulate_good_consumption(nation, total_pop):
    """
    Deduct consumer goods per population and apply stability penalty on deficit.
    """
    from provinces.building_constants import CONSUMER_GOODS_PER_POP, CONSUMER_GOODS_DEFICIT_PENALTY
    from .models import NationGoodStock, NationResourcePool

    good_stock, _ = NationGoodStock.objects.get_or_create(nation=nation)
    needed = total_pop * CONSUMER_GOODS_PER_POP
    available = good_stock.consumer_goods

    if needed <= 0:
        return

    deficit_ratio = max(0.0, (needed - available) / needed)
    good_stock.consumer_goods = max(0.0, round(available - needed, 4))
    good_stock.save()

    if deficit_ratio > 0:
        pool = NationResourcePool.objects.get(nation=nation)
        penalty = deficit_ratio * CONSUMER_GOODS_DEFICIT_PENALTY
        pool.stability = max(0.0, pool.stability - penalty)
        pool.save(update_fields=["stability"])
