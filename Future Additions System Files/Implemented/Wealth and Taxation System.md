# Wealth and Taxation System — Brainstorm

## Core Concept

**Wealth** = aggregate capacity of a nation's population to do work, scaled by how productive that work is.

**Taxation** = state's claim on surplus production, collected as **Treasury** — food-equivalent tokens spent at market prices on physical goods and labor.

---

## Prerequisite Changes

Before implementing this system:

1. **Rename `wealth` resource → `kapital`** across all code, constants, and migrations.
2. **Redesign coast terrain** — subsistence produces food (T=1.5), not kapital. Demote kapital subsistence multiplier to T=1.3.
3. **Raise non-food subsistence rate to 0.06** (food stays at 0.05). Effect: non-food base resource prices drop proportionally (~×0.833), but surpluses are unchanged (price × output is scale-invariant). Net benefit: manufactured goods become cheaper to produce (cheaper base inputs, fixed labor cost).
4. **Build national stockpile** — add `stockpile` JSONField (keyed by good key) to the `Nation` model. Updated each turn: provincial surplus flows in, government orders draw from it.

---

## Pricing: Food as Numéraire

All goods priced in **food-equivalents**. `price(food) = 1.0` always. All prices recomputed **per turn (monthly)**.

### Base Resources (Marginal Producer Dynamic Pricing)

Price set each turn by the least-productive province supplying that resource:

```
price(resource) = min_food_productivity / min_resource_productivity

min_X_productivity = min(last_turn_output / subsistence_workers)
                     across all provinces where X is primary subsistence resource
```

- Food productivity: `SUBSISTENCE_RATE_FOOD × T_agri × desg_food`
- Non-food productivity: `SUBSISTENCE_RATE_NONFOOD × T_sector × desg_resource`

Prices respond automatically to terrain, DP investment, designation changes, and population shifts — no static values.

**Canonical starting prices** (plains food T=1.5 as marginal food producer, rural desg, after non-food rate raised to 0.06):

| Resource | Best terrain (T) | Desg mod | Price (food=1.0) | Surplus margin |
|----------|-----------------|----------|------------------|----------------|
| food | plains 1.5 | 1.20 | 1.00 | 33.3% |
| materials | mountains 1.5 | 1.20 | 0.83 | 33.3% |
| energy | desert 1.4 | 1.20 | 0.89 | 28.6% |
| kapital | coast 1.3 | 0.90 | 1.11 | ~28% |

**Manpower and research are not priced.** They are special goods outside the market system — only the government can spend them, and they are not taxable. See [Special Goods](#special-goods).

### Manufactured Goods

```
production_cost(good) = [Σ(input_qty_i × price(input_i)) + workers × FOOD_CONSUMPTION_PER_POP]
                        ÷ output_qty

price(good) = production_cost(good) × shortage_factor
```

Recomputed each turn using that turn's base resource prices and shortage_factor.

- Surplus emerges when building efficiency > 1.0 baseline (traits, policies, DP)
- Shortage factor [0.5, 3.0] adds market signal when supply is constrained

### Non-Economic Goods

Research, Literacy, Security, Happiness, Stability — produced by buildings, assigned **no food-equivalent price**. Cost to produce but generate no surplus and are not taxable.

### Shortage Factor

```
# For each tradeable good G (base resources + manufactured goods):

monthly_demand[G] = (
    Σ building_input_consumption[G]        # all buildings consuming G as input this turn
    + gov_purchases[G]                      # government orders placed this turn
    + trade_exports[G]                      # outbound trade route transfers this turn
    + (pop × FOOD_CONSUMPTION_PER_POP       # food only: population subsistence demand
       if G == food else 0)
)

monthly_supply[G] = (
    Σ subsistence_output[G]                # subsistence workers producing G this turn
    + Σ building_output[G]                 # buildings producing G this turn
    + trade_imports[G]                     # inbound trade route transfers this turn
)

shortage_factor[G] = clamp(
    monthly_demand[G] / max(1, stockpile_prev[G] + monthly_supply[G]),
    0.5, 3.0
)

# Stockpile updates after all consumption resolved:
stockpile[G] = max(0, stockpile_prev[G] + monthly_supply[G] - monthly_demand[G])
```

Stockpile carried from prior turns acts as buffer — existing reserves dampen shortage spikes.

---

## Special Goods

**Manpower** and **Research** are produced by provinces but exist outside the market pricing system. They cannot be traded between nations and have no food-equivalent price. Only the government can spend them, via directed orders (military training draws manpower; research advancement draws research points). They are not taxable and do not appear in shortage_factor calculations.

---

## Treasury

**Treasury** is the government's balance of food-equivalent tokens. All tax types produce Treasury. Government spends Treasury at current market prices.

**The player sets one `tax_rate ∈ [0, 1]`.** This is the only tax rate directly controlled by the player. The four tax policy axes determine the *structure* — how that rate is applied across goods, classes, and assets.

### Collecting Treasury

All four axes apply simultaneously. Each collects Treasury independently using the player's `tax_rate` multiplied by axis-specific structure multipliers.

**Income Tax** — tax on surplus production above subsistence:
```
gross_income     = output_qty × price(resource_or_good)
subsistence_cost = workers × FOOD_CONSUMPTION_PER_POP
surplus          = max(0, gross_income - subsistence_cost)
treasury        += income_structure_rate × surplus × tax_efficiency
```
`income_structure_rate` determined by Income Tax policy rank (see Tax Policy Ranks).

**Consumption Tax** — tax on trade route transactions:
```
# Per trade route transfer each turn:
transaction_value = qty_traded × price(good)
treasury         += consumption_structure_rate[good] × transaction_value × tax_efficiency
```
`consumption_structure_rate` varies by good type per rank — importer pays the effective rate on top of market price.

**Land Tax** — tax on assessed value of owned capital:
```
# Per province per turn:
building_value  = Σ(construction_cost_food_equiv per active building)
land_value      = BASE_LAND_VALUE[terrain]
treasury       += land_structure_rate × assessed_value × tax_efficiency
```

**Gift & Estate Tax** — tax on value transfers:
```
# On receiving goods from another nation:
gift_value = qty_received × price(good)
treasury  += gift_structure_rate × gift_value

# On acquiring a province:
estate_value = building_value + BASE_LAND_VALUE[terrain]
treasury    += estate_structure_rate × estate_value
```
Gift & Estate tax is not modified by Tax Efficiency — it applies at point of transaction, not through administrative collection.

### Spending Treasury

Treasury is the only hard constraint on government orders. If goods exist in the national stockpile they are drawn from it; if not, the government acquires them at market price — scarcity is punished via `shortage_factor` raising the price, not by blocking the order.

```
order_cost = Σ(resource_qty × price(resource)) + labor × FOOD_CONSUMPTION_PER_POP
# price already incorporates shortage_factor — scarce goods cost more

# No minimum treasury check — treasury may go negative (debt accrues)
treasury     -= order_cost
stockpile[r] -= min(resource_qty[r], stockpile[r])   # draw what's available
```

Treasury accumulates across turns — players save for large expenditures.

### Debt

If treasury goes negative, debt compounds each turn:

```
if treasury < 0:
    debt = -treasury
    interest_rate = 0.02 × (1 + debt / 500)    # 2% base; doubles at 500 food-equiv debt
    treasury -= debt × interest_rate
```

At representative debt levels (nation of 20 provinces earning ~340 Treasury/turn):

| Debt | Interest rate | Charge/turn |
|------|--------------|-------------|
| 100 | 2.4% | 2.4 |
| 340 (~1 turn income) | 3.4% | 11.4 |
| 1 000 | 6.0% | 60 |
| 3 000 | 14.0% | 420 |

Small debt is survivable. Large debt compounds into fiscal crisis.

---

## Selling Stockpile Goods

Government can sell goods from the national stockpile into the market. Government receives `qty × price(good)` Treasury; stockpile decreases; supply increases in next turn's shortage_factor calculation.

```
treasury     += qty_sold × price(good)
stockpile[G] -= qty_sold
# monthly_supply[G] increases next turn → shortage_factor falls → price normalises
```

Symmetric with subsidies: subsidies inject demand (raise price), sales inject supply (lower price).

---

## Subsidies

Subsidies introduce **government demand** into the market for a class of goods. The government spends Treasury each turn to purchase a quantity at market price, raising `shortage_factor`, which raises `price(good)`, which raises producer surplus, incentivizing greater private production.

```
# Each turn, subsidy policy for good class G:
subsidy_spend   = subsidy_rate × treasury
qty_purchased   = subsidy_spend / price(G)
treasury       -= subsidy_spend
stockpile[G]   += qty_purchased

# shortage_factor sees increased demand next turn → price rises → self-corrects as supply responds
```

Subsidy classes map to existing building categories (e.g. subsidise `industry` → raises price of materials and manufactured goods drawing on materials).

---

## Tax Efficiency

Tax Efficiency (TE) is the fraction of the stated tax rate actually collected. Range `[0.01, 1.0]`. Applied to Income, Consumption, and Land taxes. **Not applied to Gift & Estate taxes** (point-of-transaction, no administrative friction).

**Control level** reduces effective TE in low-control provinces. This hook belongs in the Control & Rebellion System — wire `control_tax_multiplier(control)` into per-province tax calculation when implemented. Currently unimplemented.

```
actual_tax = tax_rate × structure_multiplier × tax_efficiency × tax_base
```

### Formula

```
tax_efficiency = 0.44 + Σ(trait_modifiers) + Σ(gov_modifiers) + building_bonus
```

Base 0.44. Calibrated so all-efficient + max buildings = exactly 1.0 and all-inefficient = exactly 0.01.

### Trait Modifiers

| Trait | Strong | Weak |
|-------|--------|------|
| `honorable` | +0.09 | +0.045 |
| `devious` | −0.09 | −0.045 |
| `collectivist` | +0.06 | +0.03 |
| `individualist` | −0.06 | −0.03 |

### Government Modifiers

**Direction axis:**
| Key | Modifier |
|-----|----------|
| `bottom_up` | +0.06 |
| `top_down` | −0.06 |
| `none` | 0 |

**Economic category axis:**
| Key | Modifier |
|-----|----------|
| `collectivist` | +0.06 |
| `resource` | −0.06 |
| `subsistence` | −0.06 |
| all others | 0 |

**Structure axis:**
| Key | Modifier |
|-----|----------|
| `hereditary` | +0.05 |
| `representative` | +0.05 |
| `power_consensus` | −0.05 |
| all others | 0 |

**Power origin axis:**
| Key | Modifier |
|-----|----------|
| `elections` | +0.05 |
| `military_power` | −0.06 |
| all others | 0 |

**Power type axis:**
| Key | Modifier |
|-----|----------|
| `singular` | +0.05 |
| `council` | +0.05 |
| `multi_body` | −0.05 |
| `staggered_groups` | −0.05 |
| all others | 0 |

### Building Bonus

`government_regulatory`, `government_management`, `government_oversight` buildings in the province increase local TE.

```
building_bonus = min(0.14, active_levels_in_province × 0.02)
```

Per-province — provinces with strong administrative infrastructure collect closer to the stated rate.

### Calibration

```
# Maximum (all efficient, strong traits, max buildings):
0.44 + 0.09 + 0.06 + 0.06 + 0.06 + 0.05 + 0.05 + 0.05 + 0.14 = 1.00

# Minimum (all inefficient, strong traits, no buildings):
0.44 − 0.09 − 0.06 − 0.06 − 0.06 − 0.05 − 0.06 − 0.05 = 0.01

# Default starting nation (subsistence + power_consensus + law_and_order + council, no traits):
0.44 − 0.06 − 0.05 + 0.05 = 0.38
```

---

## Tax Policy Ranks & Rates

The player sets one `tax_rate ∈ [0, 1]`. Each axis rank provides a structure multiplier applied to that rate. All four axes apply simultaneously.

### Income Tax

Per-province surplus = `output × price − workers × FOOD_CONSUMPTION_PER_POP`. Structure multiplier applied to that surplus.

| Rank | Structure |
|------|-----------|
| None | 0× (no income tax) |
| Flat | `tax_rate × 1.0` applied uniformly to all surplus |
| Progressive | `tax_rate × 0.5` lower class / `× 1.0` middle / `× 2.0` upper class — **stub until Class System built** |
| Regressive | `tax_rate × 1.5` lower / `× 1.0` middle / `× 0.5` upper — **stub until Class System built** |
| Wealth Redistribution | `tax_rate × 3.0` (capped 1.0) on upper class; collected Treasury redistributed to deficit provinces — **stub until Class System built** |

---

### Consumption Tax

Applied per trade route transfer. Structure determines per-good multiplier on `tax_rate`.

| Rank | Structure |
|------|-----------|
| None | 0× on all goods |
| Basic Goods Exempted | `0×` on base resources; `tax_rate × 1.5` on manufactured goods |
| All Goods | `tax_rate × 1.0` on all traded goods |
| Sin Tax | `tax_rate × 3.0` on arms, fuel, entertainment; `tax_rate × 0.5` on all other goods |
| Health Tax | `tax_rate × 2.5` on fuel, chemicals, arms; `0×` on medicine, food; `tax_rate × 0.8` on everything else |

---

### Land Tax

Applied per province per turn. Structure determines which asset base is taxed.

| Rank | Structure |
|------|-----------|
| None | 0× |
| Property Tax | `tax_rate × building_assessed_value` |
| Land Value Tax | `tax_rate × BASE_LAND_VALUE[terrain]` |
| Both | `tax_rate × 0.6 × building_value + tax_rate × 0.8 × land_value` |

Base land values (food-equiv):

| Terrain | Value |
|---------|-------|
| river_valley | 500 |
| plains | 400 |
| coast | 350 |
| urban_ruins | 300 |
| forest | 250 |
| mountains | 200 |
| desert | 150 |
| wasteland | 100 |

---

### Gift & Estate Taxes

Not subject to Tax Efficiency. Structure multipliers applied at point of transaction.

| Rank | Gift multiplier | Estate multiplier |
|------|----------------|-------------------|
| None | 0× | 0× |
| Meritocratic Intentions | `tax_rate × 0.5` | `tax_rate × 1.0` |
| Strict Meritocracy | `tax_rate × 1.0` | `min(tax_rate × 2.0, 1.0)` |
| Communal Duties | Gifts redistributed to all provinces by population share (no Treasury) | `min(tax_rate × 2.0, 1.0)` |

---

---

## Tie-Ins

| System | Hook |
|--------|------|
| Buildings | Efficiency modifiers raise surplus → raise income tax base |
| DP | `dp_mult` raises output → raises surplus → raises tax base |
| Control & Rebellion | `control_tax_multiplier(control)` reduces per-province TE in low-control provinces — **not yet implemented in control.py; add when Control System is extended** |
| Traits | `honorable`/`devious`/`collectivist`/`individualist` modify Tax Efficiency |
| Government types | All 5 gov axes contribute modifiers to Tax Efficiency |
| Government buildings | `government_regulatory`, `government_management`, `government_oversight` raise per-province TE |
| Policies | Tax type selection (all four axes); structure multipliers per rank |
| Trade | Consumption tax on route transfers; `trade_exports`/`trade_imports` feed shortage_factor |
| Military | Unit training costs debited from Treasury; manpower drawn as special good |
| Class System | Progressive, Regressive, Wealth Redistribution income tax stubs — activate when Class System built |
| Nation model | Add `stockpile` JSONField and `treasury` DecimalField |
