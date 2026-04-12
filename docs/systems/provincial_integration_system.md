# Provincial Integration System — Detailed Reference

> System 12 documentation. See `CLAUDE.md` for the system index.

## Key files

```
economy/normalization.py          — compute_ideology_mismatch(), compute_normalization_progress(),
                                    compute_normalization_penalties(), check_location_requirements(),
                                    start_normalization(), check_normalization_completion(),
                                    drift_unclaimed_ideology()
economy/integration_constants.py  — BASE_NORMALIZATION_TURNS, ECONOMIC_ACQUISITION_COSTS,
                                    PERSUADE_ACTION_DURATION, normalization penalty maxima
espionage/action_effects.py       — apply_persuade_to_join()
espionage/simulation.py           — _complete_persuade_actions() called before _expire_actions()
economy/simulation.py             — Step 6b-bis: normalization penalties; unclaimed ideology drift
turns/engine.py                   — _execute_acquisition_orders()
turns/validators.py               — _validate_acquire_province(), _validate_persuade_to_join()
```

---

### 12. Provincial Integration System

**What:** Non-core provinces carry their own `ideology_traits` when acquired. Over a normalization period they drift toward the national ideology, applying stability and happiness penalties that scale with both mismatch and remaining progress. When complete they become core provinces.

**Province fields added:**
- `ideology_traits` — JSONField `{"strong": "trait_key", "weak": ["t1", "t2"]}` (copied from nation on core; set to province's own for unclaimed/non-core)
- `is_core` — True for provinces that are fully normalized (default True for historical provinces)
- `normalization_started_turn`, `normalization_duration` — normalization timeline
- `original_nation` — FK to the nation that originally owned this province (used for reconquest shortcut)

**Normalization duration formula:**
```
Base: 120 turns (10 years)
+ Internationalist strong/weak: −48/−24 turns
+ Nationalist strong/weak: +48/+24 turns
Minimum: 12 turns (1 year)
```

**Ideology mismatch formula:**
```
Strong slot differs:  +1/3
Each weak slot missing from nation's weak set:  +1/6 each
Max: ~0.67 (strong + 2 weak differs)
```

**Normalization penalties (per turn, until normalized):**
```
stability_penalty = MAX_NORMALIZATION_STABILITY_PENALTY (15.0) × mismatch × (1 − progress)
happiness_penalty = MAX_NORMALIZATION_HAPPINESS_PENALTY (15.0) × mismatch × (1 − progress)
```

**Province acquisition mechanisms:**

| Method | Status | Notes |
|--------|--------|-------|
| economic | Implemented | Costs 2000 wealth + 1000 materials; unclaimed province only |
| espionage (`persuade_to_join`) | Implemented | FIA ≥ 2, 6 turns, unclaimed province only |
| military | Stub | Returns error |
| diplomatic | Stub | Returns error |
| conquest | Stub | Returns error |

**Location requirements** (any one of three):
1. Province borders ≥ 2 national provinces
2. Province borders ≥ 1 national province AND shares a sea/river zone with any national province
3. Province is adjacent to a sea zone AND shortest sea-zone path to a national port ≤ naval_base count

**Reconquest:** If `province.original_nation == acquiring_nation`, normalization is skipped and the province becomes core immediately.

**Order types:**
- `acquire_province` — payload `{"province_id": int, "method": "economic"}`. Deducts resources, calls `start_normalization()`.
- `espionage_action` with `action_type: "persuade_to_join"` — payload `{"action_type": ..., "target_province_id": int}`. Resolves after 6 turns.

**API endpoint:** `GET /api/games/{game_id}/nations/{nation_id}/acquirable/` — returns unclaimed provinces passing location requirements with their ideology_traits and acquisition cost.

**Serializer:** `ProvinceSerializer` now includes `ideology_traits`, `is_core`, `normalization_started_turn`, `normalization_duration`, `original_nation`, `normalization_progress` (computed from game's current_turn_number).

**Migrations:** `provinces/migrations/0009_provincial_integration.py` (adds 5 fields; data migration sets is_core=True and copies ideology_traits for all existing owned provinces)
