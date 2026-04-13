# Whitespace System — Detailed Reference

> System 15 documentation. See `CLAUDE.md` for the system index.

## Key files

```
economy/whitespace.py             — simulate_all_whitespace(), initialize_whitespace(),
                                    release_nation_provinces(), assign_random_ideology(),
                                    _simulate_whitespace_province(), _deintegrate_province(),
                                    _compute_ideology_melding()
economy/whitespace_constants.py   — BASE_DEINTEGRATION_TURNS, MELDING_RATE,
                                    MELDING_POP_DOMINANCE_RATIO, MELDING_STRONG/WEAK_WEIGHT,
                                    stub flags for future systems
economy/simulation.py             — simulate_all_whitespace() called after nation loop
economy/normalization.py          — drift_unclaimed_ideology() still used for random drift step
turns/engine.py                   — release_nation_provinces() called on nation collapse
games/views.py                    — initialize_whitespace() called on game start
provinces/models.py               — Province.deintegration_started_turn/duration fields;
                                    randomise_starting_population() updated for all 4 axes
provinces/constants.py            — RELIEF_POP_MODIFIER, VEGETATION_POP_MODIFIER,
                                    TEMPERATURE_POP_MODIFIER
provinces/serializers.py          — deintegration_started_turn, deintegration_duration,
                                    deintegration_progress added to ProvinceSerializer
```

---

### 15. Whitespace System

**What:** Provinces outside national control (`nation=None`) — shown as white on the world map. They have stable populations, independent ideologies that shift over time, and can influence adjacent provinces culturally. When a nation collapses, its provinces revert to whitespace, retaining national ideology that gradually erodes.

---

## Province fields added

- `deintegration_started_turn` — PositiveIntegerField, null. Set when a province leaves a nation. Cleared when de-integration completes.
- `deintegration_duration` — PositiveIntegerField, null. Number of turns the de-integration period lasts (default `BASE_DEINTEGRATION_TURNS = 60`).

These are separate from `normalization_started_turn`/`normalization_duration` because a province could be re-acquired mid-deintegration, requiring both state machines to run independently.

---

## Population formula

`randomise_starting_population()` now accepts all four geographic axes:

```
base = TERRAIN_BASE_POPULATION[terrain_type]
     × RELIEF_POP_MODIFIER[relief]
     × VEGETATION_POP_MODIFIER[vegetation_level]
     × TEMPERATURE_POP_MODIFIER[temperature_band]
result ∈ [base × 0.70, base × 1.30], rounded to nearest 100
```

Defaults (`flat / medium / mild`) preserve backward compatibility for callers that only pass `terrain_type`.

See `docs/balance_philosophy.md` for the full modifier table and example ranges.

---

## Game-start initialization

`initialize_whitespace(game)` is called from `GameStartView.post()` after the game transitions to ACTIVE:

- **Whitespace provinces** (nation=None): population randomized using all 4 axes; ideology assigned randomly (3 different trait pairs, 1 strong + 2 weak).
- **Owned provinces**: ideology_traits overridden to match their nation's ideology (they start fully integrated).

---

## Per-turn simulation

`simulate_all_whitespace(game, turn_number)` runs after all nation economies are simulated. For each `nation=None` province, it executes these steps in order:

### Step 1 — De-integration (if active)

Fires only for provinces recently released from nations. Drift probability increases over time:

```
progress = elapsed / duration   (0.0 → 1.0 over BASE_DEINTEGRATION_TURNS = 60 turns)
drift_chance = progress × UNCLAIMED_DRIFT_RATE × 3.0
```

- Early on (progress ≈ 0): ideology is sticky — national influence still strong.
- Late on (progress → 1): ideology drifts aggressively, approaching native whitespace.
- At completion: `deintegration_started_turn` and `deintegration_duration` are cleared.

Steps 2 and 3 are skipped for the same turn if de-integration fires.

### Step 2 — Cross-provincial ideological melding

Adjacent whitespace provinces with larger populations exert cultural pressure:

```
susceptible if: province.population < neighbor.population × MELDING_POP_DOMINANCE_RATIO (0.5)
fires if: random() < MELDING_RATE (1/24 per adjacency pair per turn)
```

When melding fires, one trait slot from the dominant neighbor is tentatively adopted. Trait-pair constraints are enforced — the 3 slots must always come from 3 different pairs.

Slot weights:
- Strong slot adoption probability: `MELDING_STRONG_WEIGHT = 0.6`
- Weak slot adoption probability: `MELDING_WEAK_WEIGHT = 0.2` (per slot, independent rolls)

### Step 3 — Random ideology drift

Only runs if the province is NOT de-integrating and melding did not fire this turn. Uses the existing `drift_unclaimed_ideology()` from `normalization.py`:

```
fires with probability: UNCLAIMED_DRIFT_RATE = 1/120 per turn
```

Picks a random slot and shifts it to a random valid trait from a different pair.

---

## Nation collapse → whitespace

`release_nation_provinces(nation, turn_number)` is called from `_check_collapse_conditions()` immediately after `nation.is_alive = False`:

- Sets `nation=None` for all provinces.
- Clears normalization fields (any in-progress normalization is abandoned).
- Sets `deintegration_started_turn = turn_number` and `deintegration_duration = 60`.
- Preserves `ideology_traits` (they remain at national alignment, eroding via de-integration).

---

## Tie-ins with other systems

| System | Interaction |
|--------|------------|
| Provincial Integration (12) | Province acquisition requires `nation=None`. De-integration state is cleared when a province is re-acquired and normalization begins. |
| Control and Rebellion (future) | Stub: `REBEL_SPAWNING_ENABLED = False`. Militarist/Nationalist whitespace provinces will eventually check for rebel spawning. |
| International Migration (future) | Stub: `WHITESPACE_MIGRATION_ENABLED = False`. Whitespace populations are currently stable (no growth or decline). |
| Population Growth (3) | Whitespace provinces do NOT run population growth simulation. Stability, security, and happiness fields are not updated per turn. |

---

## Constants summary

| Constant | Value | Meaning |
|----------|-------|---------|
| `BASE_DEINTEGRATION_TURNS` | 60 | 5 years for national ideology to fully fade |
| `MELDING_RATE` | 1/24 | ~once per 2 years per adjacency pair |
| `MELDING_POP_DOMINANCE_RATIO` | 0.5 | Province must be < 50% of neighbor's pop to be susceptible |
| `MELDING_STRONG_WEIGHT` | 0.6 | Strong trait adoption probability when melding fires |
| `MELDING_WEAK_WEIGHT` | 0.2 | Weak trait adoption probability (per slot) |
| `UNCLAIMED_DRIFT_RATE` | 1/120 | Random drift rate (from `integration_constants.py`) |
