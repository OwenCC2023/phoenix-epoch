# Population Growth — Detailed Reference

> System 3 documentation. See `CLAUDE.md` for the system index.

## Key files

```
economy/population.py   — calculate_province_growth_rate(), simulate_migration(), simulate_economic_migration()
economy/constants.py    — FOOD_CONSUMPTION_PER_POP, STABILITY_FOOD_DEFICIT_PENALTY, STABILITY_RECOVERY_RATE
```

---

### 3. Population growth — per province, three signals

**Growth rate formula** (`economy/population.py: calculate_province_growth_rate`):

```
effective_ratio = local_food_ratio + national_supplement
food_rate       = piecewise curve: -5% at ratio 0, +2% at ratio 1, plateau +5% at ratio 3+
stability_rate  = (national_stability - 50) × 0.001   (±5pp at extremes)
modifier_rate   = modifiers["growth"] flat offset  ← includes building growth_bonus per province
hard_floor      = if effective_ratio == 0: rate cannot be positive (starvation is starvation)
```

`national_supplement` converts the per-capita national food stockpile into "turns of food coverage," capped at `MAX_NATIONAL_FOOD_SUPPLEMENT = 3.0`. This means a well-stocked granary can keep non-food provinces (mountains, coasts) in the growth regime.

**Why:** Non-food provinces are *supposed* to import food; punishing them just for having no local food production would make terrain diversity pointless.
