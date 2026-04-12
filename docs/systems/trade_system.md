# Trade System — Detailed Reference

> **Full system documentation for System 13 (Trade).** See `CLAUDE.md` for the compact summary.

---

## Overview

**What:** Nation-to-nation trade routes that move a single good per route from one capital to another. Routes use Dijkstra pathfinding over the province/zone graph, consume per-domain capacity pools, and model in-flight transit (goods take multiple turns to arrive).

**Key models:** `TradeRoute`, `CapitalRelocation` (both in `trade/models.py`).

---

## Province environment fields

Three new `Province` fields gate effective land-distance multipliers:

| Field | Choices | Trade effect |
|-------|---------|-------------|
| `relief` | `flat`, `hilly`, `rugged`, `marshy`, `mountainous` | 1.0 → 1.9× distance multiplier |
| `vegetation_level` | `none`, `low`, `medium`, `high` | 1.0 → 1.3× |
| `temperature_band` | `mild`, `hot`, `cold` | 1.0 → 1.25× |

Multipliers are averaged across both endpoints of each land hop. Seeded from terrain type on migration `0009_seed_relief_from_terrain`.

Constants: `RELIEF_TYPES`, `VEGETATION_LEVELS`, `TEMPERATURE_BANDS` in `provinces/constants.py`.

---

## Key files

```
trade/constants.py         — TRADE_SPEED_PER_TURN, ZONE_HOP_DISTANCE, EMBARK_DISTANCE,
                             CAPACITY_DISTANCE_NORMALISER, capital relocation costs/delays
trade/distance.py          — effective_land_distance(), _env_mult() (relief/veg/temp averaging)
trade/pathfinding.py       — TradeGraph, PathResult, build_trade_graph(), find_shortest_path(),
                             find_trade_route_path()
trade/models.py            — TradeRoute, CapitalRelocation
trade/capacity.py          — get_trade_capacity(), route_capacity_consumption(),
                             get_used_capacity(), validate_route_capacity()
trade/capital.py           — validate_capital_relocation(), initiate_capital_relocation(),
                             process_capital_relocations(), is_wartime_capital_loss()
trade/simulation.py        — process_trade_imports(), process_trade_exports(),
                             recompute_route_paths()
trade/serializers.py       — TradeRouteSerializer, CapitalRelocationSerializer,
                             TradeRoutePreviewSerializer
trade/views.py             — TradeRouteListView, TradeRouteDetailView, TradeRoutePreviewView,
                             TradeCapacityView, CapitalRelocationView
trade/urls.py              — 5 URL patterns under /api/games/<id>/trade/
```

---

## Pathfinding

`build_trade_graph(game_id, allowed_domains)` constructs a weighted graph of province and zone nodes:

| Edge type | Domain | Building requirement |
|-----------|--------|---------------------|
| Province ↔ Province | land | none (uses `adjacent_provinces` M2M) |
| Province ↔ Sea zone | sea | `port` or `dock` active |
| Province ↔ River zone | land | none |
| Province ↔ Air zone | air | `air_cargo_terminal` active |
| Sea ↔ Sea | sea | none |
| River ↔ River | land | none |
| River ↔ Sea | sea | none |
| Air ↔ Air | air | none |

Edge weights: land uses `effective_land_distance()` (Euclidean × env mult, scaled by march speed bonus); zone hops use fixed `ZONE_HOP_DISTANCE`; embark/debark edges use `EMBARK_DISTANCE`.

`domain_mode` filter (`land`, `sea`, `air`, `multi`) restricts which edge types are included.

---

## Capacity pools

Three pools per nation: `land_trade_capacity`, `naval_trade_capacity`, `air_trade_capacity`. All are use-it-or-lose-it (recomputed from buildings each turn via `get_national_building_effects()`).

Effective capacity:
```
base × (1 + trade_pct_from_policies) × (1 + trade_capacity_bonus + trade_capacity_penalty)
```

- `trade_pct` — policy effect key (many categories have values)
- `trade_capacity_bonus` / `trade_capacity_penalty` — trait effect keys

Capacity consumed by a route per pool domain:
```
(segment_distance / CAPACITY_DISTANCE_NORMALISER) × quantity_per_turn
```

`validate_route_capacity()` returns errors if adding a new route would exceed any pool.

---

## TradeRoute model

| Field | Notes |
|-------|-------|
| `from_nation` / `to_nation` | directional; only `from_nation` can cancel |
| `good` | any key in `VALID_GOODS` (from `provinces/building_constants.py`) |
| `quantity_per_turn` | units exported each turn |
| `domain_mode` | `multi` / `land` / `sea` / `air` |
| `status` | `active` / `pending` / `inactive_war` / `broken_path` |
| `path_nodes` | JSON list of `[type, id]` nodes |
| `total_length` | total effective distance |
| `capacity_by_domain` | `{"land": float, "sea": float, "air": float}` |
| `arrival_turns` | number of turns goods are in transit |
| `in_flight` | JSON list of `{"good": str, "amount": float, "arrives_turn": int}` |
| `created_turn` | turn number when route was created |

---

## Turn integration

**`simulate_economy_for_game()`** (game-level, before per-nation loop):
1. Calls `recompute_route_paths(game, turn_number)` — updates all active/pending route paths, marks `BROKEN_PATH` or `INACTIVE_WAR`, recalculates `arrival_turns`.

**`simulate_nation_economy()`** (per-nation):
- **Step 8 (import):** `process_trade_imports()` — delivers in-flight shipments with `arrives_turn <= turn_number`. Adds to pool/good_stock immediately; recorded in `trade_net` (positive).
- **Step 16.5 (export):** `process_trade_exports()` — after `simulate_good_consumption()`, deducts from available stock (capped, no shortage triggered), pushes to `in_flight`. Also checks capital validity and marks routes `INACTIVE_WAR` if capitals are lost. Recorded in `trade_net` (negative).

`ResourceLedger` entries now include real `trade_net` values (previously always zero).

---

## Capital relocation

**`Nation.capital_province`** FK (nullable) + `get_effective_capital()` — returns the current capital, but if the province is owned by a different nation (enemy capture), returns `None`.

**`CapitalRelocation` model:** OneToOne per nation. Tracks `target_province`, `started_turn`, `completes_turn`, `cost_paid`.

| Scenario | Wealth cost | Materials cost | Delay |
|----------|------------|----------------|-------|
| Peacetime | 500 | 200 | 12 turns |
| Wartime (capital lost) | 250 | 100 | 0 turns |

`process_capital_relocations(game, current_turn)` — called from `turns/engine.py`. On completion: sets `is_capital` flags, updates `nation.capital_province`, inactivates all trade routes for that nation (`INACTIVE_WAR` status).

---

## Order types

| Order type | Payload | Validator | Engine handler |
|-----------|---------|-----------|----------------|
| `create_trade_route` | `{to_nation_id, good, quantity_per_turn, domain_mode}` | `_validate_create_trade_route()` | `_exec_create_trade_route()` |
| `cancel_trade_route` | `{route_id}` | `_validate_cancel_trade_route()` | `_exec_cancel_trade_route()` |
| `designate_capital` | `{province_id}` | `_validate_designate_capital()` | `_exec_designate_capital()` |

`create_trade_route` validation runs the pathfinder at submission time (immediate feedback to player). Route is created with status `pending`; becomes `active` on first successful `recompute_route_paths`.

---

## API endpoints

All under `/api/games/<game_id>/trade/`:

| Method | Path | View | Description |
|--------|------|------|-------------|
| GET | `routes/` | `TradeRouteListView` | List routes where nation is sender or receiver |
| GET | `routes/<id>/` | `TradeRouteDetailView` | Single route (parties only) |
| GET | `preview/` | `TradeRoutePreviewView` | Path + capacity check without creating; params: `to_nation_id`, `good`, `quantity_per_turn`, `domain_mode` |
| GET | `capacity/` | `TradeCapacityView` | Available/used/remaining per domain |
| GET | `capital-relocation/` | `CapitalRelocationView` | Pending relocation for nation |

---

## Migrations

| App | Migration | Content |
|-----|-----------|---------|
| `economy` | `0005_remove_tradeoffer.py` | Removes old `TradeOffer` model |
| `nations` | `0004_add_capital_province.py` | Adds `capital_province` FK to `Nation` |
| `provinces` | `0008_add_trade_province_fields.py` | Adds `relief`, `vegetation_level`, `temperature_band` |
| `provinces` | `0009_seed_relief_from_terrain.py` | Data migration: seeds env fields from terrain type |
| `trade` | `0001_create_traderoute_capitalrelocation.py` | Creates `TradeRoute` and `CapitalRelocation` |

---

## Key constants (`trade/constants.py`)

| Constant | Value | Purpose |
|----------|-------|---------|
| `TRADE_SPEED_PER_TURN` | 150.0 | `MARCH_SPEED × 1.5`; governs arrival turns |
| `ZONE_HOP_DISTANCE["sea"]` | 80.0 | Fixed edge weight for sea zone hops |
| `ZONE_HOP_DISTANCE["river"]` | 60.0 | Fixed edge weight for river zone hops |
| `ZONE_HOP_DISTANCE["air"]` | 120.0 | Fixed edge weight for air zone hops |
| `EMBARK_DISTANCE["sea"]` | 20.0 | Province↔sea zone edge weight |
| `EMBARK_DISTANCE["river"]` | 10.0 | Province↔river zone edge weight |
| `EMBARK_DISTANCE["air"]` | 30.0 | Province↔air zone edge weight |
| `CAPACITY_DISTANCE_NORMALISER` | 100.0 | Divides segment distance in capacity consumption formula |
| `MIN_ARRIVAL_TURNS` | 1 | Floor on transit time |
| `CAPITAL_MOVE_DELAY_TURNS` | 12 | Peacetime relocation delay |
