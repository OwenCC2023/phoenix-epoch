# Balance Philosophy

> Cross-cutting balance reference. See `CLAUDE.md` for the system index.

The calibration target is a **30-year rebuilding arc** (~360 months) with province base populations of ~3,000–12,000.

## Province starting populations (randomised ±30%)

| Terrain | Base |
|---------|------|
| river_valley | 12,000 |
| plains | 10,000 (anchor) |
| coast | 9,000 |
| urban_ruins | 8,000 |
| forest | 7,000 |
| mountains | 6,000 |
| desert | 4,000 |
| wasteland | 3,000 |

Use `provinces.models.randomise_starting_population(terrain_type)` when creating provinces — do not rely on the field default alone.

## Key calibrated constants and why

| Constant | Value | File | Reasoning |
|----------|-------|------|-----------|
| `SUBSISTENCE_RATE` | 0.05 | `provinces/jobs.py` | Plains at 10k → 900 food/turn, needs 600, surplus 300 that flows nationally |
| `FOOD_CONSUMPTION_PER_POP` | 0.06 | `economy/constants.py` | Food provinces get real surpluses; non-food deficits are proportionally manageable |
| `STABILITY_FOOD_DEFICIT_PENALTY` | 0.2/month | `economy/constants.py` | ~2.4/year; 8 months of deficit = −1.6 stability — informative not punishing |
| `STABILITY_RECOVERY_RATE` | 0.3/month | `economy/constants.py` | ~3.6/year; recovers a deficit period in ~half the time it took to lose |
| `MAX_NATIONAL_FOOD_SUPPLEMENT` | 3.0 | `economy/population.py` | Full granary can keep non-food provinces growing; rewards agricultural specialisation |
| `CONSUMER_GOODS_DEFICIT_PENALTY` | 5.0 | `provinces/building_constants.py` | 100% deficit is universal at game start; should warn, not instantly collapse |
| `URBAN_THRESHOLD` | 100,000 | `provinces/constants.py` | Plains at max growth (10%/turn) for 30 years reaches ~174k; needs buildings too |
| `URBAN_BUILDING_WEIGHT` | 15,000 | `provinces/constants.py` | 4 buildings = 60k score bonus; 4 buildings + 40k pop = urban |
| `INPUT_COLOCATION_BONUS` | 0.10 | `provinces/building_constants.py` | +10% output if any input good is locally available (terrain or supply chain) |
| `INDUSTRY_CLUSTER_BONUS` | 0.05 | `provinces/building_constants.py` | +5% per same-category peer building in province |

## The food economy in practice

A plains + mountain + coast starting nation:
- **Turn 1**: plains +4.75% growth, mountain/coast −3% (no stockpile yet)
- **Turn 3**: ~750 food stockpile → mountain/coast tip to +0.5% growth
- **Turn 8**: ~3,000 food stockpile → all provinces growing 5–7%
- This teaches the core loop fast: food specialisation feeds industrial provinces

## The industrialisation arc

| Phase | Turns (months) | Activity |
|-------|---------------|----------|
| Survival | 1–12 (year 1) | Food security, stabilise population, save for first building |
| Early industry | 6–24 (years 1–2) | Workshop L1 built → machinery → Factory L1 → consumer goods crisis resolved |
| Expansion | 24–120 (years 2–10) | More building levels, refinery, energy supply chains, population growing |
| Approaching urban | 120–360 (years 10–30) | High-growth + heavily-built provinces may urbanise; most remain rural |
