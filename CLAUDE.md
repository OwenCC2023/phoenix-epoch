# phoenix-epoch — Agent Context

## What this game is

A turn-based, asynchronous multiplayer grand-strategy game set in a **post-apocalyptic world where players rebuild industrialised societies from scratch**. The 30-year arc starts at bare subsistence and ends (for the most successful nations) at early industrialisation. Most provinces stay rural for the entire game; urban status is a genuine late-game achievement.

**Stack:** Django 4 + DRF backend (`/backend`), React + TypeScript frontend (`/frontend`), PostgreSQL, Celery for async turn resolution.

---

## Architecture overview

| App | Responsibility |
|-----|---------------|
| `accounts` | User accounts |
| `games` | Game lifecycle, turn deadline management |
| `nations` | Nation model, government, ideology traits, policies, modifiers |
| `provinces` | Province model, terrain, buildings, jobs, designation |
| `economy` | Resource pools, turn simulation engine |
| `turns` | Turn submission, resolution orchestration (Celery) |
| `espionage` | Espionage: attack/defense, transparency, actions |
| `trade` | Trade routes, Dijkstra pathfinding, capacity pools |
| `events` | GM-created events applying national modifiers |

Read the relevant system doc in `docs/systems/` before modifying a system.

---

## Systems built — index

1. [Buildings](docs/systems/buildings_system.md) — 75 types, efficiency, traits, policies
2. [Construction](docs/systems/construction_system.md) — build queue, cost/turns countdown
3. [Population growth](docs/systems/population_growth.md) — food/stability/modifier growth curve
4. [Migration](docs/systems/migration_system.md) — starvation + economic, internal/external
5. [Jobs](docs/systems/job_system.md) — subsistence vs building employment
6. [Designations](docs/systems/province_designations.md) — rural/urban/capital computed per turn
7. [Travel & zones](docs/systems/travel_system.md) — air/sea/river zones, march/embark time
8. [Security](docs/systems/security_system.md) — 0–100, policy/trait/building multipliers
9. [Happiness](docs/systems/happiness_system.md) — policy-trait alignment matrix
10. [Espionage](docs/systems/espionage_system.md) — attack/defense, transparency, 5 action types
11. [Literacy & Research](docs/systems/literacy_research_system.md) — S-curve growth, research unlocks
12. [Provincial Integration](docs/systems/provincial_integration_system.md) — normalization, acquisition
13. [Trade](docs/systems/trade_system.md) — Dijkstra routes, capacity pools, in-flight transit
14. [Bureaucratic Capacity](docs/systems/bureaucratic_capacity_system.md) — building supply, policy consumption gates, gov/trait multipliers, deficit penalties
15. [Whitespace](docs/systems/whitespace_system.md) — unclaimed province simulation, de-integration, cross-provincial ideology melding, game-start init, population formula rework (relief/vegetation/temperature modifiers)
16. [Control & Rebellion](docs/systems/control_rebellion_system.md) — per-province control (1–100%), Regions, production bonus/national flow trade-off, rebellion trigger/timer/outcomes, ideology interactions, whitespace rebel spawning
17. [Development Points](docs/systems/development_points_system.md) — per-province, per-building-category DP; logarithmic multiplier approaching 2×; concentration bonus/penalty; 40 DP/year annual grant; ALLOCATE_DP and TRANSFER_DP orders; military DP stub

**Balance philosophy** — calibrated constants, food economy, industrialisation arc → [`docs/balance_philosophy.md`](docs/balance_philosophy.md)

**Future systems & stubs** — military plan, unbuilt features, stub effect keys → [`docs/future_systems.md`](docs/future_systems.md)

---

## Turn cadence

**One turn = one month.** A full game = 360+ turns. Every rate is per month. When writing new systems: growth rates, upkeep, penalties, migration — all monthly.

---

## Balance spreadsheet — effects_matrix.xlsx

`effects_matrix.xlsx` — authoritative balance reference (Buildings, Government, Traits, Policy Effects, Legend sheets). Percentages as decimals (0.08 = 8%). Layout and workflow: [`docs/balance_spreadsheet.md`](docs/balance_spreadsheet.md).

---

## Development commands

```bash
cd backend

# Run Django dev server
DJANGO_SETTINGS_MODULE=phoenix_epoch.settings.dev ./venv/Scripts/python.exe manage.py runserver

# Run migrations
DJANGO_SETTINGS_MODULE=phoenix_epoch.settings.dev ./venv/Scripts/python.exe manage.py migrate

# Generate migrations
DJANGO_SETTINGS_MODULE=phoenix_epoch.settings.dev ./venv/Scripts/python.exe manage.py makemigrations

# Import smoke test
DJANGO_SETTINGS_MODULE=phoenix_epoch.settings.dev ./venv/Scripts/python.exe -c "import django; django.setup(); from economy.simulation import simulate_nation_economy; from trade.simulation import recompute_route_paths; from nations.bureaucratic_capacity import compute_bureaucratic_supply; from economy.dp import compute_dp_multiplier; from economy.dp_init import initialize_province_dp; print('OK')"
```

**Note:** Use `./venv/Scripts/python.exe` (not `python` — Windows Store intercept). Always set `DJANGO_SETTINGS_MODULE=phoenix_epoch.settings.dev`.

---

## Migrations status

| App | Migrations |
|-----|-----------|
| economy | 0001_initial → 0007_control_pool_snapshot |
| nations | 0001_initial → 0006_dp_pool_and_military |
| provinces | 0001_initial → 0014_development_points |
| espionage | 0001_create_espionage_models |
| trade | 0001_create_traderoute_capitalrelocation |
| All others | 0001_initial |

When adding model fields, always run `makemigrations <appname> --name descriptive_name`.

**Migration numbering:** Always verify against the actual filesystem (`ls backend/<app>/migrations/`). The table above may be ahead of `master` if a feature branch has uncommitted migrations.

---

## Building category gotchas

`SECTOR_BUILDING_CATEGORY_MAP` covers 13 building categories across 6 sectors (agriculture/extraction/industry/energy/commerce/research). These categories are **not mapped** but exist in `BUILDING_TYPES` and need explicit handling in any system that iterates all building categories:

`entertainment`, `religious`, `government_regulatory`, `government_oversight`, `government_management`, `government_security`, `government_education`, `government_organization`, `government_welfare`, `espionage_attack`, `espionage_defense`

Default weight/multiplier to 1.0 for these when distributing by sector.

---

**Codebase conventions** — circular imports, new system structure, constants files, migrations → [`docs/conventions.md`](docs/conventions.md)
