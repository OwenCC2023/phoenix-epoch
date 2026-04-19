# Development Points System (System 17)

## Overview

Development Points (DP) quantify the growing efficiency of persistent systems within a province over time. Each province accumulates DP per building category. Higher DP in a category multiplies the output of buildings in that category.

**Key mechanic:** DP applies as a **multiplier of multipliers** — it is applied multiplicatively to the final building output *after* all other efficiency bonuses (designation, traits, government, colocation, concentration). This makes it more powerful than additive efficiency bonuses.

---

## DP Categories

Each province has one DP row per non-military building category, plus one for subsistence (25 rows total):

| Sector | Building Categories |
|--------|-------------------|
| Agriculture | `farming` |
| Extraction | `extraction` |
| Industry | `heavy_manufacturing`, `light_manufacturing`, `chemical`, `construction` |
| Energy | `green_energy`, `refining` |
| Commerce | `financial`, `transport`, `communications` |
| Research | `pharmaceutical`, `healthcare` |
| Unmapped | `entertainment`, `religious`, `government_regulatory`, `government_oversight`, `government_management`, `government_security`, `government_education`, `government_organization`, `government_welfare`, `espionage_attack`, `espionage_defense` |
| Special | `subsistence` (applied to subsistence worker production, not buildings) |

**Military DP** (stub — stored, no mechanics until Combat/Doctrine systems):
- National-level categories: `strategy`, `tactics`, `logistics`

---

## Multiplier Formula

```
multiplier(dp) = 1 + dp / (dp + K)
```

Where `K = 100` (configurable in `dp_constants.py`).

| DP | Multiplier |
|----|-----------|
| 0 | 1.000× |
| 50 | 1.333× |
| 100 | 1.500× |
| 200 | 1.667× |
| 500 | 1.833× |
| 1000 | 1.909× |
| ∞ | 2.000× (limit) |

---

## Concentration Bonus/Penalty

When one category holds **>50% of a province's total DP**:

- **Concentrated category:** `1 + ((cat_dp - total_dp/2) / 50)` multiplier
- **All other categories:** `1 - ((cat_dp - total_dp/2) / 10)` multiplier (clamped to 0.0 floor)

The concentration multiplier is applied on top of the base DP multiplier.

**Note:** The penalty divisor (10) is deliberately harsh. At 60% concentration, non-concentrated sectors lose 20% output; at 75%, they lose 50%. This forces meaningful trade-offs between specialization and balanced development.

---

## Application in Simulation

### Building output (System 17 integration point)

In `economy/building_simulation.py`, the DP multiplier is applied after the final produce calculation:

```python
produce = amount × effective_capacity × designation_mult × efficiency_mult × productivity_mult
produce = produce × dp_mult   # System 17 — multiplier of multipliers
```

The `dp_mult` is looked up by building category (same key space as DP categories). Buildings with unmapped categories (e.g., espionage) still have DP rows but the building output lookup defaults to 1.0 unless DP has been explicitly allocated.

### Subsistence production

`subsistence` DP applies to the output of subsistence workers (terrain primary resource). Applied in `economy/simulation.py` Step 3, after all other subsistence modifiers.

---

## Annual DP Grant

- Nations receive **40 DP every 12 turns** (once per in-game year).
- DP accumulates in `NationDPPool.available_points`.
- Players spend from this pool via the `ALLOCATE_DP` order.
- Unspent DP carries forward indefinitely.

---

## Player Orders

### ALLOCATE_DP (annual allocation)

Submitted any turn; executed before economy simulation runs. Spends from `NationDPPool`.

```json
{
    "provincial": [
        {"province_id": 42, "category": "farming", "amount": 10},
        {"province_id": 43, "category": "heavy_manufacturing", "amount": 5}
    ],
    "military": [
        {"category": "strategy", "amount": 3}
    ],
    "expansion": 1
}
```

**Cost breakdown:**
- Provincial DP: 1:1 (10 pool points = 10 DP in category)
- Military DP: 4:1 (4 pool points = 1 military DP)
- Expansion slot: 5 pool points each

### TRANSFER_DP (intra-province reallocation)

Move DP between categories within a single province at 2:1 cost.

```json
{
    "province_id": 42,
    "source_category": "farming",
    "target_category": "heavy_manufacturing",
    "amount": 5
}
```

Spends 10 DP from `farming`, gains 5 DP in `heavy_manufacturing`.

---

## Game Start Initialization

Called from `initialize_whitespace()` in `economy/whitespace.py`.

- Each province gets **100–200 total DP** distributed across all 24 non-military building categories.
- Distribution is weighted by terrain sector multipliers (from `TERRAIN_TYPES` in `provinces/constants.py`). Building categories within a sector share that sector's terrain weight. Unmapped categories default to weight 1.0.
- Each province gets **20–40 subsistence DP** independently.
- Each nation gets a `NationDPPool` (starts at 0) and `NationMilitaryDP` rows for all three military categories (all 0).

---

## National DP Summary

`NationSerializer` includes `provincial_dp_summary` — the sum of all provincial DP per category across the nation's provinces. **Display only, no mechanical effect.**

---

## Data Models

| Model | Location | Purpose |
|-------|----------|---------|
| `ProvinceDevelopmentPoints` | `provinces/models.py` | Per-province, per-category DP (~25 rows/province) |
| `NationDPPool` | `nations/models.py` | Available unspent DP for allocation |
| `NationMilitaryDP` | `nations/models.py` | Military DP per category (stub) |

---

## Key Files

| File | Role |
|------|------|
| `economy/dp_constants.py` | All tuning constants and category lists |
| `economy/dp.py` | Pure computation (multiplier, concentration, summary) |
| `economy/dp_init.py` | Game-start initialization |
| `economy/building_simulation.py` | DP multiplier applied to building output |
| `economy/simulation.py` | Subsistence DP, annual grant, DP pre-computation |
| `turns/validators.py` | ALLOCATE_DP and TRANSFER_DP validation |
| `turns/engine.py` | ALLOCATE_DP and TRANSFER_DP execution |

---

## Constants Reference

All in `economy/dp_constants.py`:

| Constant | Value |
|----------|-------|
| `DP_MULTIPLIER_K` | 100 |
| `CONCENTRATION_BONUS_DIVISOR` | 50 |
| `CONCENTRATION_PENALTY_DIVISOR` | 10 |
| `DP_TRANSFER_COST_RATIO` | 2 |
| `DP_ANNUAL_GRANT` | 40 |
| `DP_GRANT_INTERVAL` | 12 turns |
| `DP_MILITARY_COST_RATIO` | 4 |
| `DP_EXPANSION_COST` | 5 |
| `DP_INIT_TOTAL_MIN` | 100 |
| `DP_INIT_TOTAL_MAX` | 200 |
| `DP_INIT_SUBSISTENCE_MIN` | 20 |
| `DP_INIT_SUBSISTENCE_MAX` | 40 |
