# Wealth & Taxation System (System 18)

Food-equivalent market pricing, per-nation Treasury, four parallel tax policy
axes, subsidies, and debt.  Replaces the previous flat-resource economy with
a dynamic market where all tradeable goods are priced in food-equivalents.

Spec: [`Future Additions System Files/Implemented/Wealth and Taxation System.md`](../../Future%20Additions%20System%20Files/Implemented/Wealth%20and%20Taxation%20System.md).

---

## Prerequisites (Phase 0)

1. **Rename** — the `wealth` resource key/field is renamed `kapital` across
   models, migrations, JSON data, and simulation.
2. **Coast terrain** — subsistence now produces food (`agriculture = 1.5`);
   commerce demoted to `1.3`.  Coast is food-primary.
3. **Subsistence rate split** — `SUBSISTENCE_RATE_FOOD = 0.05`,
   `SUBSISTENCE_RATE_NONFOOD = 0.06`.  `subsistence_rate_for(resource)` resolves
   the correct rate per subsistence call.

---

## Data model

| Model | Field | Purpose |
|-------|-------|---------|
| `NationResourcePool` | `treasury: Decimal(14,2)` | Government food-equivalent cash.  May go negative (debt). |
| `NationMarketSnapshot` | 1 per (nation, turn) | Records `prices`, `monthly_demand`, `monthly_supply`, `prev_subsistence_productivity`, `shortage_factors`.  Drives next turn's pricing. |
| `Nation` | `tax_rate: FloatField` | Player-set scalar `[0, 1]`. |
| `Nation` | `subsidies: JSONField` | `{sector: rate}` mapping. |

---

## Pricing (`economy/pricing.py`)

All prices are food-equivalents.  `price(food) == 1.0` always.

### Base resources (food / materials / energy / kapital)

```
price(r) = min_food_productivity / min_r_productivity
min_X_productivity = min(output / subsistence_workers)
                     across provinces where X is primary subsistence resource
```

When a resource has no subsistence producer (e.g. `kapital` post-coast
demotion), a **theoretical bootstrap** is used: best-terrain multiplier × rural
designation × `subsistence_rate_for(resource)`.

### Manufactured goods

```
unit_cost  = (Σ input_qty × input_price + workers × FOOD_CONSUMPTION_PER_POP) / output_qty
price(g)   = cheapest_producer_unit_cost(g) × shortage_factor[g]
```

### Shortage factor

```
shortage_factor[g] = clamp(
    monthly_demand[g] / max(1, prev_stockpile[g] + monthly_supply[g]),
    0.5, 3.0,
)
```

### Integration

- **Start of `simulate_nation_economy`** — `reset_accumulator(nation)`; `compute_turn_start_prices(nation)` loads prev snapshot → stores `nation._prices_this_turn`, `nation._shortage_factors_this_turn`.
- **During the turn** — `record_demand` / `record_supply` accumulate usage (called explicitly by trade/consumption hooks; subsistence + pop food are aggregated post-hoc).
- **End of turn** — `_flush_wealth_taxation_snapshot` writes a `NationMarketSnapshot` row and records min subsistence productivities for next turn.

---

## Treasury

All four tax axes apply simultaneously.  Each contributes an independent
delta.  Treasury may go negative; debt compounds at
`2% × (1 + debt / 500)` per turn.

### Spending

- `GOV_PURCHASE {good, qty}` — debit treasury at current market price, credit stockpile.
- `GOV_SELL {good, qty}` — debit stockpile, credit treasury.
- Subsidies — per-turn `rate × treasury` spent across `SUBSIDY_SECTOR_MAP[sector]` goods, recorded as demand.
- `train_unit` — charges treasury `military_goods_cost × quantity × price(military_goods)` food-equivalents.

### Debt interest — `economy.taxation.compound_debt_interest(nation)`

---

## Tax Efficiency (`nations/tax_efficiency.py`)

```
TE_province = clamp(TE_BASE + traits + gov + building_bonus, 0.01, 1.0)
```

- `TE_BASE = 0.44`
- Trait modifiers on `honorable`/`devious`/`collectivist`/`individualist` (strong ±0.09/±0.06, weak half that), registered as `tax_efficiency` keys in each trait's effects dict.
- Gov modifiers across all 5 axes (added to `_ADDITIVE_KEYS` inside `get_combined_government_effects`).
- Per-province building bonus: 0.02 per level of `government_regulatory` / `government_management` / `government_oversight` buildings, capped at 0.14.

Default starting nation (subsistence + power_consensus + law_and_order + council, no traits): **0.38**.

TE applies to Income, Consumption, and Land taxes — NOT Gift & Estate (point-of-transaction).

---

## Tax Policies (`nations/tax_policy.py`)

4 parallel axes, each picked via `policy_change` order against
`POLICY_CATEGORIES`:

| Category | Default | Ranks |
|----------|---------|-------|
| `income_tax` | flat | none, flat, progressive*, regressive*, wealth_redistribution* |
| `consumption_tax` | none | none, basic_goods_exempted, all_goods, sin_tax, health_tax |
| `land_tax` | none | none, property_tax, land_value_tax, both |
| `gift_estate_tax` | none | none, meritocratic_intentions, strict_meritocracy, communal_duties |

Ranks marked * fall back to flat until the Class System is built.

Per-rank structure multipliers are applied in `economy/taxation.py`; the
nation-level `tax_rate` is the single scalar the player sets via
`SET_TAX_RATE {new_rate}`.

---

## Tax Collection (`economy/taxation.py`)

| Collector | When | Returns |
|-----------|------|---------|
| `collect_income_tax(nation, province, prices, te, raw_production, workers)` | per-turn, per-province | Decimal surplus × structure × tax_rate × TE × control_mult |
| `collect_land_tax(nation, province, prices, te)` | per-turn, per-province | Decimal against building and/or land assessed value |
| `collect_consumption_tax(nation, good, qty, unit_price, te)` | per import (trade) | Decimal of transaction × structure × tax_rate × TE |
| `collect_gift_tax(nation, good, qty, unit_price)` | on gift receipt | Decimal, mutates treasury directly; no TE |
| `collect_estate_tax(nation, province, prices)` | on acquisition (`start_normalization`) | Decimal, mutates treasury directly; no TE |
| `compound_debt_interest(nation)` | end of turn | Decimal charge applied if treasury < 0 |

`collect_nation_turn_taxes(nation, provinces, prices, raw_productions, job_statuses)`
is the single entry point the simulator calls; it loops income + land across
provinces and applies the aggregate to treasury.

---

## Order types

| Order | Payload | Status |
|-------|---------|--------|
| `SET_TAX_RATE` | `{new_rate: float [0,1]}` | Implemented |
| `SET_SUBSIDY` | `{sector: str, rate: float [0,1]}` | Implemented |
| `GOV_PURCHASE` | `{good: str, qty: float}` | Implemented |
| `GOV_SELL` | `{good: str, qty: float}` | Implemented |
| `GIFT_RESOURCES` | `{to_nation_id: int, goods: {good: qty}}` | Implemented (applies `collect_gift_tax` on receipt) |

Executor: `TurnResolutionEngine._execute_tax_and_spending_orders(turn)`, run
after trade orders and before the economy simulation.

---

## Tie-ins

| System | Hook |
|--------|------|
| DP | `dp_mult` raises output → raises surplus → raises tax base (automatic). |
| Control & Rebellion | `economy.control.control_tax_multiplier(control) -> float` STUB (always 1.0).  Wire curve when the Control System is extended. |
| Traits | `tax_efficiency` additive effect on honorable/devious/collectivist/individualist. |
| Government | `tax_efficiency` additive effect across 11 gov axis entries; added to `_ADDITIVE_KEYS` in `get_combined_government_effects`. |
| Government buildings | Per-province TE bonus (0.02/level, cap 0.14). |
| Policies | 4 tax-policy categories; ranks resolved via `tax_policy.get_tax_structure`. |
| Trade | Consumption tax on imports; trade transfers feed the demand accumulator. |
| Military | Unit training deducts food-equivalent cost from treasury; manpower remains a special good. |
| Class System | Progressive / Regressive / Wealth-Redistribution income-tax ranks are stubs that fall back to flat. |
| Nation model | `treasury`, `tax_rate`, `subsidies`. |

---

## Known deviations from original spec

- **Kapital bootstrap price = 1.28** (not spec's 1.11).  After the Phase 0 coast
  demotion, no province has kapital as its primary subsistence resource; the
  theoretical bootstrap using `0.06 × 1.3 × 0.90 = 0.0702` is authoritative.
- **TE calibration** — spec assumed two strong ideology traits (honorable +
  collectivist, or devious + individualist) which the trait system disallows
  (one strong only).  Actual extremes: max 0.97, min 0.04 pre-clamp.  `TE_MIN
  = 0.01` catches the spec floor.
- **`policy_effects_data.py` is auto-generated** from
  `policy_effects_complete.xlsx`.  The 4 tax-policy categories were appended
  manually; they must be mirrored in the Excel source or they will be
  overwritten on the next import.
