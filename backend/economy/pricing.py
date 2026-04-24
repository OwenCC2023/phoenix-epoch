"""Food-equivalent market pricing for the Wealth & Taxation System.

All tradeable goods are priced in food-equivalents; `price(food) == 1.0` always.

Base resources (food / materials / energy / kapital) use dynamic marginal-producer
pricing: the least-productive province supplying the resource at subsistence sets
the price each turn, relative to food productivity.  When a resource has no
subsistence producer (e.g. kapital after coast is promoted to food-primary), a
theoretical best-terrain productivity is used as the bootstrap.

Manufactured goods are priced each turn at (input_cost + labor_cost) / output_qty
× shortage_factor, where input_cost uses the current base prices and
shortage_factor reflects monthly demand vs supply plus carried stockpile.

Usage:
    from economy.pricing import (
        load_prev_market_snapshot,
        compute_base_resource_prices,
        compute_manufactured_good_prices,
        compute_shortage_factors,
        compute_min_productivities_from_data,
        flush_market_snapshot,
        record_demand,
        record_supply,
    )
"""
from __future__ import annotations

from typing import Any, Iterable

from provinces.constants import (
    DESIGNATION_SUBSISTENCE_MODIFIERS,
    SECTOR_RESOURCE_MAP,
    TERRAIN_TYPES,
)
from provinces.jobs import subsistence_rate_for, terrain_primary_resource
from provinces.building_constants import BUILDING_TYPES, get_level_data

from .constants import FOOD_CONSUMPTION_PER_POP
from .pricing_constants import (
    BASIC_RESOURCES,
    BASIC_RESOURCES_SET,
    SHORTAGE_FACTOR_MAX,
    SHORTAGE_FACTOR_MIN,
    SPECIAL_GOODS,
)


# --- Demand / supply accumulation -----------------------------------------

def _accum(nation) -> dict:
    """Lazy per-nation in-memory accumulator for demand/supply totals this turn."""
    acc = getattr(nation, "_market_accum", None)
    if acc is None:
        acc = {"demand": {}, "supply": {}}
        nation._market_accum = acc
    return acc


def reset_accumulator(nation) -> None:
    nation._market_accum = {"demand": {}, "supply": {}}


def record_demand(nation, good: str, qty: float) -> None:
    if not qty or good in SPECIAL_GOODS:
        return
    d = _accum(nation)["demand"]
    d[good] = d.get(good, 0.0) + float(qty)


def record_supply(nation, good: str, qty: float) -> None:
    if not qty or good in SPECIAL_GOODS:
        return
    s = _accum(nation)["supply"]
    s[good] = s.get(good, 0.0) + float(qty)


def get_accumulated(nation) -> tuple[dict, dict]:
    acc = _accum(nation)
    return dict(acc["demand"]), dict(acc["supply"])


# --- Base resource productivity helpers -----------------------------------

def _sectors_for_resource(resource_key: str) -> list[str]:
    """Return all sector keys that map to the given resource (e.g. materials
    is produced by both 'extraction' and 'industry')."""
    return [s for s, r in SECTOR_RESOURCE_MAP.items() if r == resource_key]


def _theoretical_min_productivity(resource_key: str) -> float:
    """Per-worker output if the best-terrain province at rural designation
    produced this resource at subsistence.  Used as a bootstrap when no
    province actually has this resource as its primary subsistence output."""
    sectors = _sectors_for_resource(resource_key)
    if not sectors:
        return 0.0
    best_t = 0.0
    for tdef in TERRAIN_TYPES.values():
        mults = tdef.get("multipliers", {})
        for sector in sectors:
            t = mults.get(sector, 0.0)
            if t > best_t:
                best_t = t
    if best_t <= 0:
        return 0.0
    desg_mod = DESIGNATION_SUBSISTENCE_MODIFIERS["rural"].get(resource_key, 1.0)
    return subsistence_rate_for(resource_key) * best_t * desg_mod


def compute_min_productivities_from_data(
    provinces: Iterable, job_statuses: dict, raw_productions: dict
) -> dict[str, float]:
    """Given this turn's data, return min subsistence productivity per basic resource.

    Parameters
    ----------
    provinces : iterable of Province
    job_statuses : {province_id: dict from get_province_job_status}
    raw_productions : {province_id: {resource_key: produced_qty}}
    """
    per_resource: dict[str, list[float]] = {r: [] for r in BASIC_RESOURCES}
    for p in provinces:
        primary = terrain_primary_resource(p.terrain_type)
        if primary not in BASIC_RESOURCES_SET:
            continue
        js = job_statuses.get(p.id)
        raw = raw_productions.get(p.id, {})
        if not js:
            continue
        sub_workers = js.get("subsistence_workers", 0)
        if sub_workers <= 0:
            continue
        produced = raw.get(primary, 0.0)
        if produced <= 0:
            continue
        per_resource[primary].append(produced / sub_workers)
    out = {}
    for r in BASIC_RESOURCES:
        values = per_resource[r]
        out[r] = min(values) if values else _theoretical_min_productivity(r)
    return out


# --- Price computations ----------------------------------------------------

def compute_base_resource_prices(min_productivities: dict) -> dict[str, float]:
    """Return {resource_key: price_in_food_equiv} given min productivities.

    price(food) = 1.0 (numéraire).
    price(r)    = min_food_productivity / min_r_productivity
    """
    food_prod = float(min_productivities.get("food") or _theoretical_min_productivity("food"))
    if food_prod <= 0:
        food_prod = subsistence_rate_for("food") * 1.5 * 1.20  # last-resort fallback
    out = {"food": 1.0}
    for r in BASIC_RESOURCES:
        if r == "food":
            continue
        rp = float(min_productivities.get(r) or _theoretical_min_productivity(r))
        out[r] = (food_prod / rp) if rp > 0 else 0.0
    return out


def compute_shortage_factors(
    prev_stockpile: dict, monthly_demand: dict, monthly_supply: dict
) -> dict[str, float]:
    """Return {good: shortage_factor ∈ [SHORTAGE_FACTOR_MIN, SHORTAGE_FACTOR_MAX]}.

    shortage = demand / max(1, prev_stockpile + this_turn_supply)
    """
    out: dict[str, float] = {}
    keys = set(monthly_demand) | set(monthly_supply) | set(prev_stockpile)
    for g in keys:
        if g in SPECIAL_GOODS:
            continue
        demand = float(monthly_demand.get(g, 0.0))
        supply = float(prev_stockpile.get(g, 0.0)) + float(monthly_supply.get(g, 0.0))
        ratio = demand / max(1.0, supply)
        out[g] = max(SHORTAGE_FACTOR_MIN, min(SHORTAGE_FACTOR_MAX, ratio))
    return out


def _cheapest_producer_unit_cost(
    good: str, base_prices: dict, cached: dict[str, float]
) -> float:
    """Return the cheapest per-unit production cost for `good` across all
    level-1 buildings that output it.  Recursive for chained intermediates."""
    if good in cached:
        return cached[good]
    cached[good] = float("inf")  # guard against cycles
    best = float("inf")
    for b_key, b_def in BUILDING_TYPES.items():
        try:
            ld = get_level_data(b_key, 1)
        except Exception:
            continue
        outputs = ld.get("outputs", {})
        if good not in outputs:
            continue
        out_qty = float(outputs[good])
        if out_qty <= 0:
            continue
        inputs = ld.get("inputs", {}) or {}
        workers = float(ld.get("workers", 0))
        input_cost = 0.0
        for in_good, in_qty in inputs.items():
            if in_good in BASIC_RESOURCES_SET:
                p = float(base_prices.get(in_good, 1.0))
            else:
                # Recursive — but guarded by `cached` above to prevent infinite recursion.
                p = _cheapest_producer_unit_cost(in_good, base_prices, cached)
                if p == float("inf"):
                    p = 1.0  # fallback: treat unknown intermediate as food-priced
            input_cost += float(in_qty) * p
        labor_cost = workers * FOOD_CONSUMPTION_PER_POP
        unit_cost = (input_cost + labor_cost) / out_qty
        if unit_cost < best:
            best = unit_cost
    cached[good] = best
    return best


def compute_manufactured_good_prices(
    base_prices: dict, shortage_factors: dict, good_keys: Iterable[str]
) -> dict[str, float]:
    """Return {good: price_in_food_equiv} for each manufactured good.

    price = production_cost × shortage_factor (default 1.0 if good not in shortage_factors).
    """
    cached: dict[str, float] = {}
    out: dict[str, float] = {}
    for good in good_keys:
        cost = _cheapest_producer_unit_cost(good, base_prices, cached)
        if cost == float("inf"):
            out[good] = 1.0
            continue
        sf = float(shortage_factors.get(good, 1.0))
        out[good] = cost * sf
    return out


# --- Snapshot load / flush -------------------------------------------------

def load_prev_market_snapshot(nation):
    """Return the most recent NationMarketSnapshot for this nation, or None."""
    from .models import NationMarketSnapshot  # local import to avoid circulars
    return (
        NationMarketSnapshot.objects.filter(nation=nation).order_by("-turn_number").first()
    )


def compute_turn_start_prices(nation, good_keys: Iterable[str] | None = None) -> dict:
    """Compute prices used *this* turn from the previous turn's snapshot.

    Returns dict with keys 'prices' and 'shortage_factors'.
    Safe to call before the first turn has been simulated (uses theoretical bootstrap).
    """
    from provinces.building_constants import GOOD_KEYS as MFG_GOOD_KEYS
    prev = load_prev_market_snapshot(nation)
    if prev is None:
        min_prod = {r: _theoretical_min_productivity(r) for r in BASIC_RESOURCES}
        prev_stockpile: dict = {}
        prev_demand: dict = {}
        prev_supply: dict = {}
    else:
        min_prod = dict(prev.prev_subsistence_productivity or {})
        prev_stockpile = _stockpile_as_dict(nation)
        prev_demand = dict(prev.monthly_demand or {})
        prev_supply = dict(prev.monthly_supply or {})
    base_prices = compute_base_resource_prices(min_prod)
    shortage = compute_shortage_factors(prev_stockpile, prev_demand, prev_supply)
    mfg_keys = list(good_keys) if good_keys is not None else list(MFG_GOOD_KEYS)
    mfg_prices = compute_manufactured_good_prices(base_prices, shortage, mfg_keys)
    all_prices = {**base_prices, **mfg_prices}
    return {"prices": all_prices, "shortage_factors": shortage}


def _stockpile_as_dict(nation) -> dict:
    """Return current national stockpile across base pool + manufactured goods."""
    from .models import NationGoodStock
    pool = getattr(nation, "resource_pool", None)
    out: dict[str, float] = {}
    if pool is not None:
        for r in BASIC_RESOURCES:
            out[r] = float(getattr(pool, r, 0) or 0)
    stocks = NationGoodStock.objects.filter(nation=nation).first()
    if stocks is not None:
        from provinces.building_constants import GOOD_KEYS
        for g in GOOD_KEYS:
            out[g] = float(getattr(stocks, g, 0) or 0)
    return out


def flush_market_snapshot(
    nation,
    turn_number: int,
    prices: dict,
    monthly_demand: dict,
    monthly_supply: dict,
    prev_subsistence_productivity: dict,
    shortage_factors: dict,
):
    """Persist a snapshot row.  Safe to call once per nation per turn.

    Idempotent on (nation, turn_number) — overwrites if one already exists.
    """
    from .models import NationMarketSnapshot
    snap, _ = NationMarketSnapshot.objects.update_or_create(
        nation=nation,
        turn_number=turn_number,
        defaults={
            "prices": {k: float(v) for k, v in prices.items()},
            "monthly_demand": {k: float(v) for k, v in monthly_demand.items()},
            "monthly_supply": {k: float(v) for k, v in monthly_supply.items()},
            "prev_subsistence_productivity": {
                k: float(v) for k, v in prev_subsistence_productivity.items()
            },
            "shortage_factors": {k: float(v) for k, v in shortage_factors.items()},
        },
    )
    return snap
