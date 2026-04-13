# Control, Regions, and Rebellion System (System 16)

## Overview

Control is a per-province value (1–100%, default 100%) that gates how much of provincial production flows to the national government. It also affects rebellion risk, normalization speed, and espionage defence. Regions are logical groupings of provinces that share a single control level.

**Core trade-off:** Tight control (100%) delivers maximum national revenue but forfeits a production bonus. Loose control boosts local output by up to +25% but a smaller fraction reaches the national pool.

---

## Key Files

| File | Purpose |
|------|---------|
| `economy/control_constants.py` | All numeric constants for control and rebellion |
| `economy/control.py` | Pure computation functions (production bonus, flow fraction, ideology interactions) |
| `economy/rebellion.py` | Rebellion trigger, rebel spawning, suppression check, outcome resolution |
| `provinces/models.py` | `Region` model; `Province.control`, `Province.region`, rebellion fields |
| `nations/models.py` | `Nation.player` nullable, `Nation.is_npc` flag (for rebel independence) |
| `economy/models.py` | `ControlPoolSnapshot` — informational per-turn snapshot |
| `economy/simulation.py` | Control wiring (Steps 3, 5, 6, 11.5, 18.5) |
| `espionage/simulation.py` | Control defense/transparency wiring |
| `provinces/views.py` | Region CRUD, province control PATCH, rebellion list |
| `nations/urls.py` | Region and rebellion URL patterns |
| `provinces/urls.py` | Province control PATCH URL |

---

## Province Fields

| Field | Type | Description |
|-------|------|-------------|
| `control` | FloatField(default=100.0) | Effective control level (1–100) |
| `region` | FK(Region, nullable) | Region this province belongs to, if any |
| `is_rebel_occupied` | BooleanField | True while rebels hold the province |
| `rebel_timer_start_turn` | PositiveIntegerField(nullable) | Turn rebels spawned |
| `rebel_timer_duration` | PositiveIntegerField(nullable) | Turns the nation has to suppress (3–5) |

---

## Region Model

```python
class Region(models.Model):
    nation    = FK(Nation)
    name      = CharField(max_length=100)
    control   = FloatField(default=100.0)   # 1.0–100.0
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("nation", "name")
```

Regions are purely logical groupings — provinces need not be geographically contiguous. When a region's control is updated, `sync_region_control(region)` pushes the value to all member provinces (denormalized to `Province.control` for join-free simulation).

---

## Control Formulas

| Formula | Description |
|---------|-------------|
| `control / 100.0` | National flow fraction — fraction of surplus exported to the nation |
| `0.25 × (1 − control/100)` | Production bonus on materials, energy, wealth (not food/manpower) |
| `2 ** ((100 − control) / 40)` | Normalization time multiplier (doubles every 40% below 100%) |
| `control / 100.0` | Espionage defence multiplier |
| `0.30 × (1 − control/100)` | Foreign transparency bonus from weak governance |

At 100% control: full flow, no production bonus, no normalization penalty, full defence.  
At 60% control: 60% flow, +10% production, 2× normalization time, 0.60× defence.  
At 1% control: 1% flow, +24.75% production, ~5.3× normalization time, +30% transparency.

---

## Rebellion Mechanics

### Trigger (all three required simultaneously)
1. `province.local_stability < 20`
2. `province.local_happiness < 20`
3. `ideology_mismatch(province, nation) > 0.5`

A province already in rebellion cannot trigger a second one.

### Rebel Formation
- Created by `spawn_rebel_formation(province, turn_number)`
- Formation named `"Rebel Forces — {province.name}"`, owned by the **nation** (appears in nation military tracking)
- Unit type `"rebel"` — zero cost, zero upkeep, cannot be recruited by players
- Quantity = `max(1, int(population × 0.002))`
- Timer: random 3–5 turns

### Suppression (Stub)
- `check_rebel_suppression(province)` returns True if any non-rebel formation in the province has `effective_strength` greater than total rebel strength
- Full combat resolution deferred to the Combat System

### Rebel Victory Outcomes (weighted random)

| Outcome | Base Weight | Description |
|---------|------------|-------------|
| `whitespace` | 3 | Province reverts to whitespace (de-integration begins) |
| `join_neighbor` | 2 | Province joins the most ideology-aligned adjacent nation |
| `independence` | 1 | Province forms a new NPC nation (`is_npc=True, player=None`) |

If the best adjacent nation has ideology mismatch < 0.3, `join_neighbor` weight gets +3 bonus.  
If `join_neighbor` is chosen but no matching neighbor exists, falls back to `whitespace`.

### Per-Turn Tick
`process_rebellion_tick(provinces, nation, turn_number)`:
1. Non-occupied provinces: check trigger → spawn rebels
2. Rebel-occupied: check suppression → clear if suppressed
3. Rebel-occupied mid-timer: check expiry → resolve victory

---

## Ideology-Control Interactions

| Trait | Effect | Scale |
|-------|--------|-------|
| Libertarian | +up to 5 stability recovery, +up to 5 happiness at minimum control | Strong: 1×, Weak: 0.5× |
| Authoritarian | National happiness penalty (sum of `0.5 × (100 − control)/100` per province, capped at 15) | Strong: 1×, Weak: 0.5× |
| Egalitarian | National happiness bonus (up to +8) when province controls are uniform; degrades as stdev increases | Strong: 1×, Weak: 0.5× |

---

## Rebel-Occupied Province Behaviour

- **No production** — `raw_production` is zeroed in Step 3
- **No export** — exported dict stays empty in Step 5
- **No national food** — effective_food = 0.0 (province receives no food distribution)
- **Stability crashes** — food_ratio=0 drives stability below the rebellion threshold
- Security, happiness, and literacy continue to compute (deteriorate naturally)
- Province `control`, `is_rebel_occupied`, timer fields saved in `update_fields` each turn

---

## Pool Tracking

`ControlPoolSnapshot` (informational, does not affect gameplay):

| Field | Meaning |
|-------|---------|
| `tax_revenue_total` | Wealth production × integration |
| `tax_revenue_retained` | × (1 − control/100) — stays at province/region level |
| `trade_capacity_total` | (Materials + Energy) × integration |
| `bc_total` | Research × integration |
| `research_total` | Same as bc_total |

Provinces in a region are aggregated into a single row per region per turn. Provinces outside any region each get their own row.

---

## Whitespace Rebel Spawning

When `REBEL_SPAWNING_ENABLED = True` (enabled in `whitespace_constants.py`), whitespace provinces with **militarist** or **nationalist** ideology (strong or weak) have a 2% chance per turn of spawning an ownerless rebel band:

- Formation name: `"Armed Band — {province.name}"`, `nation=None`
- Quantity = `max(1, int(population × 0.001))`
- Stub for future combat/occupation mechanics

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET/POST | `/api/games/{game_id}/nations/{nation_id}/regions/` | List/create regions |
| GET | `/api/games/{game_id}/nations/{nation_id}/regions/{pk}/` | Region detail |
| PATCH | `/api/games/{game_id}/nations/{nation_id}/regions/{pk}/` | Update name/control (syncs to provinces) |
| DELETE | `/api/games/{game_id}/nations/{nation_id}/regions/{pk}/` | Delete region |
| POST | `/api/games/{game_id}/nations/{nation_id}/regions/{pk}/add-province/` | Add province to region |
| POST | `/api/games/{game_id}/nations/{nation_id}/regions/{pk}/remove-province/` | Remove province from region |
| PATCH | `/api/games/{game_id}/provinces/{pk}/control/` | Set individual province control (400 if in region) |
| GET | `/api/games/{game_id}/nations/{nation_id}/rebellions/` | List rebel-occupied provinces |

---

## Future Stubs

- **Partisan rebels** (`spawn_partisan_rebels`) — no-op until the Occupation System is built; set `PARTISAN_SPAWN_ENABLED = True` to activate
- **Combat-based suppression** — `check_rebel_suppression()` is a stub; replace with proper combat resolution when the Combat System is built
- **Whitespace migration** — `WHITESPACE_MIGRATION_ENABLED` flag in `whitespace_constants.py`

---

## Migrations

| App | Migration | Description |
|-----|-----------|-------------|
| provinces | `0013_region_and_control` | Region model; Province control, region FK, rebellion fields |
| nations | `0005_region_and_control` | Nation.player nullable, Nation.is_npc |
| economy | `0007_control_pool_snapshot` | ControlPoolSnapshot model |
