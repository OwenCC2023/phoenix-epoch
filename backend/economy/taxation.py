"""Tax collection + debt interest for the Wealth & Taxation System.

All collectors return a `Decimal` delta to the nation's treasury.  They do NOT
mutate state — callers are responsible for `nation.resource_pool.treasury +=
result` and saving.  Exception: collectors whose spec calls for "at point of
transaction" (gift_tax, estate_tax) mutate treasury directly because they fire
outside the per-turn simulation loop (order executor / normalization).

Structure multipliers per rank live in the spec doc; see
`nations/tax_policy.py` for category → rank → structure-key maps.

Tax Efficiency (TE) scales Income / Consumption / Land taxes (administrative
friction).  Gift & Estate taxes bypass TE — they apply at transaction time.
"""
from __future__ import annotations

from decimal import Decimal

from provinces.building_constants import BUILDING_TYPES, get_level_data

from .constants import FOOD_CONSUMPTION_PER_POP
from .pricing_constants import (
    BASE_LAND_VALUE,
    BASIC_RESOURCES_SET,
    DEBT_INTEREST_BASE,
    DEBT_INTEREST_SCALE,
    HARMFUL_GOODS,
    MEDICINE_GOODS,
    SIN_GOODS,
)


def _D(x) -> Decimal:
    """Coerce float/int → Decimal with 2-dp rounding via string form."""
    return Decimal(f"{float(x):.2f}")


# --- Income Tax -----------------------------------------------------------

_INCOME_STRUCTURE_MULT = {
    "none":                 0.0,
    "flat":                 1.0,
    "progressive":          1.0,   # STUB — Class System; falls back to flat
    "regressive":           1.0,   # STUB — Class System; falls back to flat
    "wealth_redistribution":1.0,   # STUB — Class System; falls back to flat
}


def collect_income_tax(
    nation,
    province,
    prices: dict,
    te_province: float,
    raw_production: dict | None = None,
    subsistence_workers: int | None = None,
) -> Decimal:
    """Return the income-tax contribution from this province.

    surplus = Σ(output × price) − workers × FOOD_CONSUMPTION_PER_POP
    treasury += structure × tax_rate × surplus × TE × control_multiplier
    """
    from nations.tax_policy import income_tax_structure
    from .control import control_tax_multiplier

    structure = income_tax_structure(nation)
    struct_mult = _INCOME_STRUCTURE_MULT.get(structure, 0.0)
    if struct_mult <= 0:
        return Decimal("0.00")

    if raw_production is None:
        # Fall back to current ProvinceResources — last turn's saved output.
        from provinces.models import ProvinceResources
        try:
            res = ProvinceResources.objects.get(province=province)
            raw_production = {
                "food": res.food or 0, "materials": res.materials or 0,
                "energy": res.energy or 0, "kapital": res.kapital or 0,
                "manpower": res.manpower or 0, "research": res.research or 0,
            }
        except ProvinceResources.DoesNotExist:
            return Decimal("0.00")

    # Gross income from priced outputs only (manpower/research not priced).
    gross = 0.0
    for good, qty in raw_production.items():
        if good in ("manpower", "research"):
            continue
        price = float(prices.get(good, 1.0))
        gross += float(qty) * price

    workers = subsistence_workers
    if workers is None:
        workers = int(province.population or 0)
    subsistence_cost = float(workers) * FOOD_CONSUMPTION_PER_POP
    surplus = max(0.0, gross - subsistence_cost)
    if surplus <= 0:
        return Decimal("0.00")

    ctrl_mult = control_tax_multiplier(_province_control(province))
    tax_rate = float(nation.tax_rate or 0)
    raw = struct_mult * tax_rate * surplus * float(te_province) * ctrl_mult
    return _D(raw)


# --- Land Tax -------------------------------------------------------------

def _assessed_building_value(province) -> float:
    """Sum of construction-cost food-equivalents for active completed buildings.

    Uses `base_construction_cost` at building's level via get_level_data.
    Materials + kapital costs are combined 1:1 in food-equivalents for the
    purpose of this assessment (spec uses a flat assessed value; tax structure
    picks the exact base).
    """
    total = 0.0
    qs = province.buildings.filter(is_active=True, under_construction=False)
    for b in qs:
        try:
            ld = get_level_data(b.building_type, max(1, int(b.level or 1)))
        except Exception:
            continue
        cost = ld.get("cost", {}) or {}
        for _k, v in cost.items():
            total += float(v)
    return total


def _land_value(province) -> float:
    return float(BASE_LAND_VALUE.get(province.terrain_type, 0))


def collect_land_tax(nation, province, prices: dict, te_province: float) -> Decimal:
    """Return land-tax contribution from this province.

    Structure:
      property_tax    → tax_rate × building_value
      land_value_tax  → tax_rate × BASE_LAND_VALUE[terrain]
      both            → tax_rate × (0.6 × building + 0.8 × land)
    """
    from nations.tax_policy import land_tax_structure
    from .control import control_tax_multiplier

    structure = land_tax_structure(nation)
    if structure == "none":
        return Decimal("0.00")

    bldg_val = _assessed_building_value(province)
    land_val = _land_value(province)

    if structure == "property_tax":
        base = bldg_val
    elif structure == "land_value_tax":
        base = land_val
    elif structure == "both":
        base = 0.6 * bldg_val + 0.8 * land_val
    else:
        return Decimal("0.00")

    tax_rate = float(nation.tax_rate or 0)
    ctrl_mult = control_tax_multiplier(_province_control(province))
    raw = tax_rate * base * float(te_province) * ctrl_mult
    return _D(raw)


# --- Consumption Tax ------------------------------------------------------

def consumption_structure_rate(nation, good: str) -> float:
    """Per-good structure multiplier on `nation.tax_rate` for consumption tax."""
    from nations.tax_policy import consumption_tax_structure

    structure = consumption_tax_structure(nation)
    if structure == "none":
        return 0.0
    if structure == "all_goods":
        return 1.0
    if structure == "basic_goods_exempted":
        return 0.0 if good in BASIC_RESOURCES_SET else 1.5
    if structure == "sin_tax":
        return 3.0 if good in SIN_GOODS else 0.5
    if structure == "health_tax":
        if good in HARMFUL_GOODS:
            return 2.5
        if good in MEDICINE_GOODS or good == "food":
            return 0.0
        return 0.8
    return 0.0


def collect_consumption_tax(
    nation, good: str, qty: float, unit_price: float, te_nation: float
) -> Decimal:
    """Return consumption tax on a single trade transfer.

    Special goods (manpower, research) are never taxed — they are outside the
    market pricing system.
    """
    from .pricing_constants import SPECIAL_GOODS
    if good in SPECIAL_GOODS:
        return Decimal("0.00")
    struct_mult = consumption_structure_rate(nation, good)
    if struct_mult <= 0:
        return Decimal("0.00")
    tax_rate = float(nation.tax_rate or 0)
    transaction_value = float(qty) * float(unit_price)
    raw = struct_mult * tax_rate * transaction_value * float(te_nation)
    return _D(raw)


# --- Gift & Estate ---------------------------------------------------------

def _gift_structure_mult(nation) -> float:
    from nations.tax_policy import gift_estate_structure
    s = gift_estate_structure(nation)
    if s == "meritocratic_intentions":
        return 0.5
    if s == "strict_meritocracy":
        return 1.0
    if s == "communal_duties":
        return 0.0   # gifts redistributed, not taxed to treasury (stub)
    return 0.0


def _estate_structure_mult(nation) -> float:
    from nations.tax_policy import gift_estate_structure
    s = gift_estate_structure(nation)
    if s == "meritocratic_intentions":
        return 1.0
    if s in ("strict_meritocracy", "communal_duties"):
        return 2.0
    return 0.0


def collect_gift_tax(nation, good: str, qty: float, unit_price: float) -> Decimal:
    """Point-of-transaction tax on gifts received.  Mutates `nation.resource_pool.treasury`
    and returns the amount added (positive) to treasury.

    No TE applied.  Communal Duties stub returns 0 (redistribution not implemented).
    """
    struct = _gift_structure_mult(nation)
    if struct <= 0:
        return Decimal("0.00")
    tax_rate = float(nation.tax_rate or 0)
    value = float(qty) * float(unit_price)
    amount = _D(struct * tax_rate * value)
    _apply_treasury_delta(nation, amount)
    return amount


def collect_estate_tax(nation, province, prices: dict) -> Decimal:
    """Point-of-transaction tax on province acquisition.

    value = Σ building_value + BASE_LAND_VALUE[terrain]
    Mutates `nation.resource_pool.treasury`, returns the amount added.
    Structure multiplier is capped at 1.0 for strict_meritocracy/communal_duties
    (so the 2.0 × tax_rate can't exceed 1.0 of value).
    """
    struct = _estate_structure_mult(nation)
    if struct <= 0:
        return Decimal("0.00")
    tax_rate = float(nation.tax_rate or 0)
    eff = min(1.0, struct * tax_rate)
    value = _assessed_building_value(province) + _land_value(province)
    amount = _D(eff * value)
    _apply_treasury_delta(nation, amount)
    return amount


# --- Debt interest --------------------------------------------------------

def compound_debt_interest(nation) -> Decimal:
    """If treasury < 0, compound interest for this turn.  Returns the charge
    applied (positive).  Mutates `nation.resource_pool.treasury`.

    interest_rate = DEBT_INTEREST_BASE × (1 + debt / DEBT_INTEREST_SCALE)
    charge = debt × interest_rate
    """
    from .models import NationResourcePool
    pool, _ = NationResourcePool.objects.get_or_create(nation=nation)
    treasury = Decimal(pool.treasury or 0)
    if treasury >= 0:
        return Decimal("0.00")
    debt = float(-treasury)
    rate = DEBT_INTEREST_BASE * (1.0 + debt / DEBT_INTEREST_SCALE)
    charge = _D(debt * rate)
    pool.treasury = treasury - charge
    pool.save(update_fields=["treasury"])
    return charge


# --- Helpers --------------------------------------------------------------

def _province_control(province) -> float:
    """Return the province's control level (0–100).  Safe default 100 if
    the Control system isn't tracking this province."""
    try:
        from .control import get_province_control
        return float(get_province_control(province))
    except Exception:
        return 100.0


def _apply_treasury_delta(nation, delta: Decimal) -> None:
    from .models import NationResourcePool
    pool, _ = NationResourcePool.objects.get_or_create(nation=nation)
    pool.treasury = Decimal(pool.treasury or 0) + delta
    pool.save(update_fields=["treasury"])


# --- Simulation integration hook ------------------------------------------

def collect_nation_turn_taxes(nation, provinces, prices, raw_productions, job_statuses) -> Decimal:
    """Loop income + land collection across all provinces.  Returns total added
    to treasury (positive).  Mutates `nation.resource_pool.treasury`.
    """
    from nations.tax_efficiency import (
        compute_nation_tax_efficiency_base,
        compute_province_tax_efficiency,
    )
    nation_base = compute_nation_tax_efficiency_base(nation)
    total = Decimal("0.00")
    for p in provinces:
        te = compute_province_tax_efficiency(nation_base, p)
        rp = raw_productions.get(p.id, {}) if raw_productions else {}
        js = job_statuses.get(p.id, {}) if job_statuses else {}
        sub_workers = js.get("subsistence_workers") if js else None
        total += collect_income_tax(nation, p, prices, te, rp, sub_workers)
        total += collect_land_tax(nation, p, prices, te)
    if total != 0:
        _apply_treasury_delta(nation, total)
    return total
