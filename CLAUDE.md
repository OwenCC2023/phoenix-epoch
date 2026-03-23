# phoenix-epoch — Agent Context

## What this game is

A turn-based, asynchronous multiplayer grand-strategy game set in a **post-apocalyptic world where players rebuild industrialised societies from scratch**. The 30-year arc starts at bare subsistence and ends (for the most successful nations) at early industrialisation. Most provinces stay rural for the entire game; urban status is a genuine late-game achievement.

**Stack:** Django 4 + DRF backend (`/backend`), React + TypeScript frontend (`/frontend`), PostgreSQL, Celery for async turn resolution.

---

## Architecture overview

### Backend apps

| App | Responsibility |
|-----|---------------|
| `accounts` | User accounts |
| `games` | Game lifecycle (lobby → active → paused → finished), turn deadline management |
| `nations` | Nation model, government type, ideology traits, policies, national modifiers |
| `provinces` | Province model, terrain types, buildings, job system, designation |
| `economy` | Resource pools, simulation engine, population growth, migration, construction, building production |
| `turns` | Turn submission, resolution orchestration (Celery tasks) |
| `events` | GM-created game events that apply modifiers |

### Key files to read before changing economy logic

```
economy/simulation.py            — main turn loop, calls everything in order
economy/population.py            — growth curve, starvation migration, economic migration
economy/building_simulation.py   — building production, efficiency system, effect helpers
economy/construction.py          — construction tick, completion
provinces/jobs.py                — job capacity, subsistence vs building employment, designation
provinces/constants.py           — terrain definitions, designation thresholds & modifiers
provinces/building_constants.py  — BUILDING_TYPES dict, per-level workers/inputs/outputs/costs/effects
provinces/travel_constants.py    — travel speed constants, cross-type requirements, zone speed keys
provinces/travel.py              — get_march_time(), get_embark_time(), get_zone_travel_time(), check_cross_type_requirements()
economy/constants.py             — FOOD_CONSUMPTION_PER_POP, stability penalties, government types
nations/trait_constants.py       — 18 ideology traits in 9 pairs, trait effects, validation
nations/government_constants.py  — five-axis GOV_* dicts, GOV_COMPONENTS, get_combined_government_effects()
nations/policy_constants.py      — 67 policy categories with discrete levels + POLICY_EFFECTS, POLICY_REQUIREMENTS, POLICY_BANS, BUILDING_POLICY_REQUIREMENTS, BUILDING_POLICY_BANS, UNIT_POLICY_REQUIREMENTS, UNIT_POLICY_BANS
nations/policy_effects.py        — get_nation_policy_effects(), validate_policy_change(), get_policy_building_blocks(), get_policy_unit_blocks()
```

---

## Systems built (as of 2026-03-22)

### 1. Buildings system

**What:** Each province can have up to one building of each type. Buildings consume workers from the province population, consume input goods each turn, and produce output goods.

**75 building types** across 23 categories:

| Category | Buildings |
|----------|-----------|
| `financial` | trading_post, bank, stock_exchange |
| `light_manufacturing` | factory, textile_mill, electronics_factory, precision_workshop |
| `heavy_manufacturing` | workshop, arms_factory, heavy_forge, industrial_complex, shipyard |
| `refining` | refinery, advanced_refinery, fuel_depot, biofuel_plant |
| `chemical` | chemical_plant, fertilizer_plant, plastics_factory |
| `pharmaceutical` | pharmaceutical_lab, medical_supply_depot, research_institute |
| `farming` | irrigation_network, grain_silo, agricultural_station |
| `extraction` | mine, oil_well, logging_camp |
| `construction` | construction_yard, cement_plant, infrastructure_bureau |
| `transport` | road_network, railway_station, logistics_hub, dock, port, bridge, railroad, train_depot, train_station, train_cargo_terminal, airport, air_cargo_terminal |
| `communications` | radio_tower, telegraph_network, broadcasting_station |
| `entertainment` | tavern, theatre, resort |
| `healthcare` | clinic, hospital, sanitation_works |
| `religious` | church, madrasa, holy_site |
| `green_energy` | wind_farm, solar_array, hydroelectric_dam |
| `government_regulatory` | regulatory_office, standards_bureau |
| `government_oversight` | inspector_general, audit_commission |
| `government_management` | civil_service_academy, administrative_center |
| `government_security` | police_headquarters, intelligence_agency |
| `government_education` | public_school, university |
| `government_organization` | labor_bureau, workers_council |
| `government_welfare` | social_services_office, public_housing |
| `military_education` | military_academy, naval_war_college, air_force_academy |

**Why designed this way:** The production chain creates a bootstrapping problem — you can't run a factory without machinery, and you can't make machinery without a workshop. This mirrors real industrialisation and gives the game a natural progression arc.

**Key model:** `Building` (provinces app). Unique per (province, building_type). Has `level`, `is_active`, `under_construction`, `construction_turns_remaining`.

**Manufactured goods** tracked in `NationGoodStock`: `consumer_goods`, `arms`, `fuel`, `machinery`, `chemicals`, `medicine`, `components`, `heavy_equipment`. Basic resources produced by buildings (food, materials, energy, wealth, research) go to `NationResourcePool`.

**Use-it-or-lose-it effects:** `land_trade_capacity`, `naval_trade_capacity`, `air_trade_capacity`, and `bureaucratic_capacity` are computed fresh each turn from active buildings (summed nationally via `get_national_building_effects()`). They are NOT stockpiled. Financial buildings provide `land_trade_capacity` as a national effect. The old `trade_capacity` key has been split into three domain-specific keys.

**Building output formula:**
```
output = amount × effective_capacity × designation_mult × efficiency_mult
```
where `effective_capacity = min(worker_capacity_factor, input_goods_capacity)`.

### 1a. Building effects (province/national bonuses from buildings)

Each building level can declare an `effects` dict. Effect keys split into two scopes:

**Province scope** (applied per-province during the simulation loop):
- `farming_bonus` — multiplier on food subsistence output
- `research_bonus` — multiplier on research output
- `integration_bonus` — additional fraction of province surplus reaching national pool
- `growth_bonus` — flat monthly addition to population growth rate
- `stability_recovery_bonus` — addition to monthly stability recovery rate
- `construction_time_reduction` — fraction reduction in construction turns *(stub — not yet wired into build API)*
- `literacy_bonus` — multiplier for province literacy rate *(stub — not yet wired)*
- `march_speed_bonus` — province-scope land travel speed modifier (road_network, railway_station)
- `sea_transit_speed` — province-scope sea embarkation speed modifier (dock, port)
- `river_transit_speed` — province-scope river crossing speed modifier (dock, bridge)
- `air_transit_speed` — province-scope air transition speed modifier (airport)

**National scope** (summed across all provinces, applied nationally each turn):
- `upkeep_reduction` — fraction reduction in government upkeep
- `construction_cost_reduction` — fraction reduction in construction costs *(stub — not yet wired into build API)*
- `bureaucratic_capacity` — total bureaucratic capacity (use-it-or-lose-it, stub)
- `land_trade_capacity` — total land trade capacity from financial + ground transport buildings
- `naval_trade_capacity` — total naval trade capacity from port/dock buildings
- `air_trade_capacity` — total air trade capacity from airport/air_cargo_terminal buildings
- `march_speed_bonus` — national land travel speed modifier (logistics_hub, railroad, train_depot; also military_academy)
- `sea_transit_speed` — national sea-to-sea travel speed modifier (also naval_war_college)
- `river_transit_speed` — national river-to-river travel speed modifier
- `air_transit_speed` — national air-to-air travel speed modifier (also air_force_academy)
- `army_training_speed_bonus` — reduces army unit training turns *(stub — wired when military sim built)*
- `navy_training_speed_bonus` — reduces navy unit training turns *(stub)*
- `air_training_speed_bonus` — reduces air unit training turns *(stub)*
- `army_combat_bonus` — army combat effectiveness multiplier *(stub — wired when combat built)*
- `navy_combat_bonus` — navy combat effectiveness multiplier *(stub)*
- `air_combat_bonus` — air combat effectiveness multiplier *(stub)*
- `army_upkeep_reduction` — fraction reduction in army unit upkeep *(stub)*
- `navy_upkeep_reduction` — fraction reduction in navy unit upkeep *(stub)*
- `air_upkeep_reduction` — fraction reduction in air unit upkeep *(stub)*

**Note on dual-scope keys:** `march_speed_bonus`, `sea_transit_speed`, `river_transit_speed`, and `air_transit_speed` appear in **both** `PROVINCE_EFFECT_KEYS` and `NATIONAL_EFFECT_KEYS`. Province-scope values apply only to that province's cross-type transitions; national-scope values apply globally to same-type zone travel.

Helper functions: `get_province_building_effects(province)` and `get_national_building_effects(provinces)` in `economy/building_simulation.py`.

### 1b. Building efficiency — multi-source modifier system

`efficiency_mult = 1.0 + sum(all additive bonuses)` applied to building **output only** (not inputs). Six sources, each separately additive:

| # | Source | Where defined | Scope |
|---|--------|--------------|-------|
| 1 | **Government type** | `GOVERNMENT_TYPES["building_efficiency"]` | National, per category — 2-3 entries per government type |
| 2 | **Trait bonuses** | `TRAIT_DEFS[trait]["*_effects"]["building_efficiency_bonus"]` | National, per category — varies by trait selection |
| 2b | **Policy bonuses** | `POLICY_EFFECTS[cat][level]["base"]["building_efficiency_bonus"]` | National, per category — from active policy levels |
| 3 | **GM crisis/boon** | `NationModifier(category="building_efficiency", target=…)` | National, target = category name or `"all"` |
| 4 | **Input co-location** | `INPUT_COLOCATION_BONUS = 0.10` | Per-building: fires if ANY input good is locally available — either the province terrain's primary resource, or a good produced by another active building in the same province |
| 5 | **Industry cluster** | `INDUSTRY_CLUSTER_BONUS = 0.05` | Per-building: +5% per other active same-category building in province |

**Key function:** `compute_building_efficiency()` in `economy/building_simulation.py`.

**Government building_efficiency bonuses:**

| Government | Bonus 1 | Bonus 2 | Bonus 3 |
|-----------|---------|---------|---------|
| democracy | financial +10% | communications +8% | |
| autocracy | heavy_manufacturing +10% | extraction +8% | |
| theocracy | farming +8% | healthcare +10% | religious +12% |
| junta | construction +10% | heavy_manufacturing +8% | |
| tribal | farming +12% | extraction +8% | |
| corporate | financial +12% | transport +8% | |
| commune | farming +10% | light_manufacturing +8% | |

**Trait building_efficiency bonuses:** Several traits provide `building_efficiency_bonus` dicts in their effects. These are merged from the nation's 3 selected traits (1 strong + 2 weak, each with different magnitudes). See `nations/trait_constants.py` for the full definitions. Example traits with efficiency bonuses: militarist (heavy_manufacturing, chemical), positivist (communications, pharmaceutical), ecologist (farming, extraction, green_energy), industrialist (heavy_manufacturing, refining), spiritualist (religious, healthcare), etc.

**GM modifier usage:** Create a `NationModifier` with `category="building_efficiency"`, `target="chemical"` (any category) or `"all"`, `value=-0.25` (crisis) or `+0.20` (boon). Expiry via normal `expires_turn`.

**Co-location examples:**
- Workshop (needs `materials`) in a mountain province (produces materials) → +10%
- Factory (needs `materials`, `energy`, `machinery`) in a province with a workshop (which produces `machinery`) → +10% from supply-chain co-location
- Pharmaceutical lab (needs `chemicals`) in a province with a chemical plant → +10% from supply-chain co-location
- Co-location fires once regardless of how many inputs match.

**Cluster example:** Three chemical buildings in one province — each gets +2 × 5% = +10% cluster bonus.

### 1c. Military colleges — nation-unique buildings

Three buildings in the `military_education` category. Each is **nation-unique** (`unique_per_nation: True`): only one may exist across all of a nation's provinces regardless of province. Enforcement is in `BuildingView.post` — checks `Building.objects.filter(province__nation=..., building_type=...)` before allowing L1 construction.

| Building | Placement | Upkeep inputs (L3) | Key effects (L3) |
|----------|-----------|--------------------|-----------------|
| `military_academy` | Any province | wealth 1400 + research 350 + consumer_goods 400 | army_training_speed +25%, army_combat +13%, march_speed +8%, army_upkeep_reduction 13% |
| `naval_war_college` | **Coastal only** | wealth 1400 + research 350 + fuel 400 | navy_training_speed +25%, navy_combat +13%, sea_transit +8%, navy_upkeep_reduction 13% |
| `air_force_academy` | Any province | wealth 1400 + research 380 + fuel 280 + components 160 | air_training_speed +25%, air_combat +13%, air_transit +8%, air_upkeep_reduction 13% |

Effects are nationwide (all national-scope). Bonuses were halved relative to province-scoped equivalents to reflect the broader coverage.

Construction cost (all three, L1/L2/L3): ~5000 materials + 4000–16000 wealth; 24–56 turns. The `march_speed_bonus`, `sea_transit_speed`, and `air_transit_speed` effects stack with the travel system (system 7) and the transport buildings.

**Combat/upkeep reduction effects are stubs** — reserved in `NATIONAL_EFFECT_KEYS` for when the military simulation is built. Training speed effect keys follow the same naming convention as the existing `training_speed_bonus` in `nations/trait_constants.py` (per-branch variants).

### 1d. Ideology Traits system

**What:** Replaced the old single-ideology system. Each nation selects **3 traits from 3 different pairs** (9 pairs, 18 traits total): **1 strong trait** (full bonuses) + **2 weak traits** (reduced bonuses).

**Storage:** `Nation.ideology_traits` JSONField: `{"strong": "militarist", "weak": ["industrialist", "nationalist"]}`

**Key files:**
- `nations/trait_constants.py` — `TRAIT_PAIRS`, `TRAIT_DEFS`, `validate_trait_selection()`, `get_effective_trait_effects()`
- `nations/helpers.py` — `get_nation_trait_effects(nation)` merges strong+weak effects
- `economy/simulation.py` — wires trait effects into production, stability, growth, upkeep
- `economy/building_simulation.py` — trait `building_efficiency_bonus` is source 2 in efficiency system

**Trait effect types (wired into simulation):**
- `stability_bonus/penalty` — flat national stability adjustment
- `growth_bonus/penalty` — per-month population growth rate
- `integration_bonus` — stacks with base integration efficiency
- `research_bonus/penalty` — percentage modifier on research production
- `manpower_bonus` — percentage modifier on manpower production
- `wealth_production_bonus` — percentage modifier on wealth production
- `food_production_bonus` — percentage modifier on food production
- `upkeep_reduction` — fraction reduction in government upkeep
- `rural_output_bonus/penalty` — subsistence output multiplier in rural provinces
- `urban_output_bonus` — building output multiplier in urban provinces (TODO: wire in building_simulation)
- `urban_growth_penalty` — per-month growth penalty in urban provinces
- `urban_threshold_reduction` — flat reduction to URBAN_THRESHOLD score
- `building_efficiency_bonus` — dict of building category → bonus (wired into efficiency system)
- `building_restrictions` — list of building types that cannot be constructed

**Stub effects (awaiting future systems):** trade_capacity, diplomatic_reputation, espionage, bureaucratic_capacity, happiness, literacy, military_organisation, etc.

### 1e. Policies system

**What:** 67 policy categories, each with 2-10 discrete levels. One row per (nation, category) in `NationPolicy` model. Policy effects are fully wired into the simulation and building system.

**Key files:**
- `nations/policy_constants.py` — `POLICY_CATEGORIES`, `POLICY_EFFECTS`, `POLICY_REQUIREMENTS`, `POLICY_BANS`, `BUILDING_POLICY_REQUIREMENTS`, `BUILDING_POLICY_BANS`, `UNIT_POLICY_REQUIREMENTS`, `UNIT_POLICY_BANS`
- `nations/policy_effects.py` — `get_nation_policy_effects()`, `validate_policy_change()`, `get_policy_building_blocks()`, `get_policy_unit_blocks()`
- `nations/models.py` — `NationPolicy` model
- `nations/helpers.py` — `create_default_policies(nation)` bulk-creates defaults on nation creation

**Policy changes:** Submitted as orders via `policy_change` order type with `change_type: "policy_level"`, `category`, and `new_level`. Validated in `turns/validators.py` (calls `validate_policy_change()`), executed in `turns/engine.py`.

**Policy effects — fully wired.** `get_nation_policy_effects(nation)` merges active policy effects into a flat dict using a three-layer system:

1. **`base`** — unconditional numeric effects applied to all nations at that policy level
2. **`government_modifiers`** — keyed by five-axis government values (see below); all matching axis values are applied additively
3. **`trait_modifiers`** — keyed by ideology trait; all matching nation traits are applied additively

**Five-axis government_modifiers keys:** The Nation model has five orthogonal government fields. `government_modifiers` keys in `POLICY_EFFECTS` must use valid axis values from one of these five axes:

| Axis field | Valid values |
|-----------|-------------|
| `gov_direction` | `top_down`, `bottom_up`, `none` |
| `gov_economic_category` | `liberal`, `collectivist`, `protectionist`, `resource`, `autarkic`, `subsistence` |
| `gov_structure` | `hereditary`, `power_consensus`, `federal`, `representative`, `direct` |
| `gov_power_origin` | `elections`, `economic_success`, `law_and_order`, `military_power`, `religious`, `ideology` |
| `gov_power_type` | `singular`, `council`, `large_body`, `multi_body`, `staggered_groups` |

A nation can match multiple `government_modifiers` keys simultaneously (e.g., `collectivist` economy + `elections` origin both fire if present). This is intentional. When adding new `government_modifiers` entries, **never use old legacy type names** (`junta`, `democracy`, `autocracy`, etc.) — they will silently never match.

**Legacy type → axis value mapping (for reference):**
`democracy→elections`, `autocracy→singular`, `junta→military_power`, `commune→collectivist`, `tribal→subsistence`, `theocracy→religious`, `corporate→liberal`

**Effect keys wired into simulation** (`economy/simulation.py`):
- `stability_bonus/penalty` — flat national stability
- `growth_bonus/penalty` — per-month growth rate
- `integration_bonus` — stacks with base integration efficiency
- `research_bonus/penalty`, `manpower_bonus`, `wealth_production_bonus`, `food_production_bonus`
- `upkeep_reduction` — fraction reduction in government upkeep
- `building_efficiency_bonus` — dict of building category → bonus (source 2b in efficiency system, applied in `building_simulation.py`)
- `army_training_speed_bonus`, `navy_training_speed_bonus`, `air_training_speed_bonus` — stub keys (wired when military sim built)
- `army_upkeep_reduction`, `navy_upkeep_reduction`, `air_upkeep_reduction` — stub keys

**`POLICY_REQUIREMENTS`:** Gates which nations may select a given level. Keys: `gov_axis_required` (must have at least one of these axis values), `gov_axis_banned` (must not have any), `traits_required`, `traits_banned`, `policies_required`.

**`POLICY_BANS`:** Cross-policy incompatibilities. When a nation has `(cat, level)`, the listed `(cat, level)` pairs become unavailable.

**`BUILDING_POLICY_REQUIREMENTS` / `BUILDING_POLICY_BANS`:** `get_policy_building_blocks(nation)` returns the set of building types blocked by current policies. Called in `provinces/views.py BuildingView.post` before allowing construction.

**`UNIT_POLICY_REQUIREMENTS` / `UNIT_POLICY_BANS`:** `get_policy_unit_blocks(nation)` returns the set of unit types blocked. Called in `turns/validators.py _validate_train_unit` (stub — integrate when military sim is built).

### 2. Construction system

Buildings have a construction cost (paid immediately from `NationResourcePool`) and a `construction_turns` countdown. Each turn `process_construction_tick()` advances all under-construction buildings. The player can queue one building upgrade per province at a time. `get_nation_under_construction()` provides the construction queue for the UI.

`get_construction_modifiers(nation)` in `building_simulation.py` aggregates the national `construction_cost_reduction` from active buildings — ready to wire into the build API when needed.

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

### 4. Migration — two processes

**Starvation migration** (`simulate_migration`): provinces with negative growth rate lose population proportional to `|rate| × MIGRATION_RATE`. If any province is growing → internal (national total conserved). If *all* provinces are declining → external (migrants leave the nation; national total shrinks).

**Economic migration** (`simulate_economic_migration`): subsistence workers in provinces with no unfilled building jobs migrate to provinces with unfilled building slots, *if* the destination is not declining. Always internal. Rate = `ECONOMIC_MIGRATION_RATE = 0.02` (per month).

### 5. Job system

Two tiers of employment per province:

- **Subsistence**: all workers not in buildings. Produce the terrain's *primary resource* at `SUBSISTENCE_RATE × terrain_best_multiplier`. Deliberately low productivity.
- **Building jobs**: each active completed building provides `workers` slots. Workers fill building slots before doing subsistence. Partial staffing → `worker_capacity_factor < 1.0` → buildings operate at reduced output.

Extensible via `_JOB_CAPACITY_PROVIDERS` registry in `provinces/jobs.py`.

### 6. Province designations

Computed each turn and persisted on `Province.designation`. Priority order:

1. **`capital`** — always, if `is_capital = True`. Government-building bonuses are a future stub.
2. **`urban`** — score ≥ threshold (standard: 100,000; urban_ruins: 40,000). Score = pop + active_buildings × 15,000. Requires sustained high growth AND investment.
3. **`post_urban`** — `urban_ruins` terrain below the urban threshold. Ruins of a former city; has a research/wealth lean.
4. **`rural`** — everything else. The default for the entire 30-year game for most provinces.

**Modifiers** (see `DESIGNATION_SUBSISTENCE_MODIFIERS` and `DESIGNATION_BUILDING_MODIFIER` in `provinces/constants.py`):

- Rural: +20% primary producers (food/materials/energy), −10% wealth/research
- Urban: −10–15% primary producers, +20% wealth/research, building output ×1.2
- Post-urban: moderate, +15% research, building output ×1.1
- Capital: similar to urban, +15% wealth/research, building output ×1.15

### 7. Province zone adjacency & travel time system

**What:** Provinces now have a geographic graph. Three zone types exist alongside province-to-province adjacency. Travel time functions underpin the future combat and trade systems.

**Three zone models** (in `provinces/models.py`, before `Province`):
- `AirZone` — game-scoped; self-referential M2M adjacency
- `SeaZone` — game-scoped; M2M to other SeaZones and to AirZones; reverse FK from RiverZone
- `RiverZone` — game-scoped; FK to SeaZone (which sea it drains to); M2M to other RiverZones and AirZones

**Province fields added:**
- `center_x`, `center_y` — abstract map coordinates (nullable until map is developed)
- `sea_border_distance`, `river_border_distance` — distance from center to the relevant border edge (nullable)
- `air_zone` — FK to AirZone (SET_NULL)
- `adjacent_provinces` — symmetrical M2M self-referential
- `adjacent_sea_zones` — M2M to SeaZone
- `adjacent_river_zones` — M2M to RiverZone

**Key files:**
```
provinces/travel_constants.py  — MARCH_SPEED, EMBARK_SPEED, BASE_ZONE_TRAVEL, FREE_CROSS_TYPE_TRANSITIONS,
                                  CROSS_TYPE_REQUIREMENTS (OR-group structure), speed modifier key maps
provinces/travel.py            — get_march_time(), get_embark_time(), get_zone_travel_time(),
                                  check_cross_type_requirements()
```

**Travel time formulas:**
- Province→Province: `distance(centers) / (MARCH_SPEED × (1 + march_speed_bonus))` — falls back to `DEFAULT_MARCH_TIME = 1.0` when coordinates are null
- Province↔Sea/River: `border_distance / (EMBARK_SPEED × (1 + transit_speed_bonus))` — falls back to `DEFAULT_EMBARK_TIME = 0.1`; with `EMBARK_SPEED = 1000` and typical distances of 5–20 map units this gives 0.005–0.02 turns
- Zone→Zone (same type): `BASE_ZONE_TRAVEL[type] / (1 + zone_speed_bonus)` — base is 1.0 turn for all three types
- Free (zero-cost) transitions: sea↔air, river↔air

**Cross-type requirements:** `CROSS_TYPE_REQUIREMENTS` uses an OR-group structure (`list[list[str]]`). Province↔sea requires `dock`. Province↔air requires `air_base` **or** `airport`. Province↔river has no requirement.

**Transport building placement restrictions** (enforced in `BuildingView.post`):
- `dock`, `port` — coastal provinces only
- `bridge` — river provinces only

**9 new transport buildings** and their primary effects:
| Building | Province scope | National scope |
|----------|---------------|----------------|
| dock | sea_transit_speed, river_transit_speed | — |
| port | sea_transit_speed | naval_trade_capacity |
| bridge | river_transit_speed | land_trade_capacity |
| railroad | march_speed_bonus | land_trade_capacity |
| train_depot | — | land_trade_capacity, march_speed_bonus |
| train_station | march_speed_bonus | land_trade_capacity |
| train_cargo_terminal | — | land_trade_capacity |
| airport | air_transit_speed | air_trade_capacity |
| air_cargo_terminal | — | air_trade_capacity |

**API endpoints** (under `/api/games/{game_id}/provinces/`):
- `GET zones/air/` → AirZoneListView
- `GET zones/sea/` → SeaZoneListView
- `GET zones/river/` → RiverZoneListView

Serializers return adjacency as ID lists (not nested) to avoid recursive graph serialisation.

**Admin:** All three zone types registered with `filter_horizontal` for M2M adjacency management. `ProvinceAdmin` updated with `air_zone` display and M2M adjacency filter widgets.

---

## Turn cadence

**One turn = one month.** A full game lasts 30+ years = **360+ turns.**

Every rate in the codebase is expressed per month. Annual equivalents are shown in comments where relevant. When writing new systems: growth rates, upkeep, penalties, migration rates — all monthly.

---

## Balance philosophy

The calibration target is a **30-year rebuilding arc** (~360 months) with province base populations of ~3,000–12,000.

### Province starting populations (randomised ±30%)

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

### Key calibrated constants and why

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

### The food economy in practice

A plains + mountain + coast starting nation:
- **Turn 1**: plains +4.75% growth, mountain/coast −3% (no stockpile yet)
- **Turn 3**: ~750 food stockpile → mountain/coast tip to +0.5% growth
- **Turn 8**: ~3,000 food stockpile → all provinces growing 5–7%
- This teaches the core loop fast: food specialisation feeds industrial provinces

### The industrialisation arc

| Phase | Turns (months) | Activity |
|-------|---------------|----------|
| Survival | 1–12 (year 1) | Food security, stabilise population, save for first building |
| Early industry | 6–24 (years 1–2) | Workshop L1 built → machinery → Factory L1 → consumer goods crisis resolved |
| Expansion | 24–120 (years 2–10) | More building levels, refinery, energy supply chains, population growing |
| Approaching urban | 120–360 (years 10–30) | High-growth + heavily-built provinces may urbanise; most remain rural |

---

## Future systems (planned but not built)

### Research / technology tree
Research is produced today (urban_ruins, technocratic ideology) but accumulates unused. Intended to unlock building upgrades, government transitions, or national bonuses. Design not yet settled.

### Military system
**A full design plan exists at `C:\Users\miloc\.claude\plans\military-system.md` — read it before implementing any part of this system.**

The plan covers: Weapons Factory building, Army/Naval/Air Base buildings, MilitaryUnit model, per-base unit construction queues, base synergy stacking, Province `is_coastal`/`is_river` attributes, military upkeep in simulation, Militarist/Pacifist trait wiring, and the full `train_unit` order type. Implementation order and verification commands are included.

Summary of what needs to be built:
- **`military_goods`** — new manufactured good (Weapons Factory: arms + machinery + components → military_goods)
- **Province attributes** — `is_coastal`, `is_river` BooleanFields (required for Naval Base placement)
- **3 base building types** — `army_base`, `naval_base` (coastal/river only), `air_base` in new military categories
- **11 unit types** — 5 army, 3 navy, 3 air; trained by bases consuming military_goods + manpower
- **MilitaryUnit model** — province FK, unit_type, quantity (active), in_training, construction_turns_remaining
- **Base synergy** — each base level in a province reduces other bases' training time by 5%
- **Military upkeep** — deducted per active unit per turn; units go inactive on deficit (not destroyed)
- **Pacifist** → adds `weapons_factory` to building_restrictions; **Militarist** → base efficiency bonuses + training_speed_bonus

### Bureaucratic capacity
The `capital` designation is a stub. Once built, government buildings in the capital should provide bureaucratic capacity that enables larger nations (higher integration efficiency, more provinces before administrative penalties, etc.).

### Trade system
`trade_net` in the `ResourceLedger` is always zeroed. The `TradeOffer` model exists. Trade execution between nations is the next economy feature.

### Events system
`GameEvent` model and `events/helpers.py` exist. GM-created events can apply national modifiers. Not yet integrated into turn resolution loop.

### Province control / conquest
No combat system yet. Provinces can be reassigned via admin, but there is no player-facing conquest mechanic.

### Construction cost/time reduction (wiring stub)
`construction_cost_reduction` (national) and `construction_time_reduction` (province) effects are computed by buildings but not yet applied in the build API. `get_construction_modifiers(nation)` in `building_simulation.py` aggregates cost reduction and is ready to call from the construction view.

---

## Balance spreadsheet — effects_matrix.xlsx

`effects_matrix.xlsx` in the repo root is the authoritative balance reference. It has five sheets:

| Sheet | Content |
|-------|---------|
| Buildings | Per-building, per-level effects at L1 (all 75 buildings) |
| Government Options | Per-axis-value effects for the five government axes |
| Traits | Per-trait effects (strong and weak rows separate) |
| Policy Effects | Per-policy-level effects (base, gov modifier, trait modifier rows) |
| Legend | Colour key and scale notes |

All numeric cells are real numbers (not text). Percentages are stored as decimals (0.08 = 8%) with a `+0.0%;-0.0%` format. Flat values use `+0.0;-0.0` or integer format. Cell colours: green = positive wired effect, red = negative wired effect, yellow = stub (declared but not yet wired), blue row = first entry in a new category group.

### Column layout (all sheets share this structure)

| Cols | Group | Key effects mapped here |
|------|-------|------------------------|
| 1–4 | Labels | Source Type, Name, Category/Axis, Notes |
| 5–15 | Province Effects | stability_recovery_bonus, growth, farming_bonus, research_bonus, integration_bonus, construction_time_reduction, march/sea/river/air transit |
| 16–21 | National Capacity | land/naval/air trade capacity, bureaucratic_capacity, upkeep_reduction, construction_cost_reduction |
| 22–30 | Military (stub) | army/navy/air training speed, combat bonus, upkeep reduction |
| 31–42 | Gov & Trait Modifiers | stability (flat), growth/turn, integration %, trade %, research %, military %, consumption %, production food/materials/wealth/energy/manpower % |
| 43–65 | Building Efficiency | one column per building category (financial, light_manufacturing … military_education) |
| 66–76 | Trait Effects | manpower %, wealth_prod %, food_prod %, rural/urban output, urban growth penalty, urban_threshold, training speed, mil upkeep, building restrictions |
| 77–84 | Stubs | trade cap, diplo rep, espionage, arms prod |

### Policy Effects sheet row structure

Each row represents one effect source for one policy level:

| Col | Content |
|-----|---------|
| A (Source Type) | `Policy Base` / `Policy Gov Mod` / `Policy Trait Mod` |
| B (Name) | `{Category Name} -- {Level Name}` |
| C (Category) | Policy category name (human-readable) |
| D (Notes) | `base` | `when gov: {axis_value}` | `when trait: {trait_key}` |
| E–CF | Effect values |

Rows with no effects are omitted. First row of each policy category is blue; subsequent rows for the same category are light gray.

### Regenerating the Policy Effects sheet

```bash
cd backend
DJANGO_SETTINGS_MODULE=phoenix_epoch.settings.dev ./venv/Scripts/python.exe ../tools/export_policy_effects.py
```

`tools/export_policy_effects.py` reads `POLICY_CATEGORIES` and `POLICY_EFFECTS` from `nations/policy_constants.py` and rewrites only the Policy Effects sheet, leaving the other sheets untouched.

After regenerating, run the numbers-stored-as-text cleanup pass if any new string values were introduced:

```python
# one-liner cleanup (run from backend/ with Django setup)
import re, openpyxl
wb = openpyxl.load_workbook('../effects_matrix.xlsx')
pct_re = re.compile(r'^([+-]?\d+\.?\d*)%$')
flat_re = re.compile(r'^([+-]?\d+\.?\d*)$')
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            if not isinstance(cell.value, str): continue
            m = pct_re.match(cell.value.strip())
            if m:
                cell.value = float(m.group(1)) / 100
                cell.number_format = '+0.0%;-0.0%;0.0%'; continue
            m = flat_re.match(cell.value.strip())
            if m:
                v = float(m.group(1))
                cell.value = v
                cell.number_format = '+0.0;-0.0;0.0' if '.' in m.group(1) else '+#,##0;-#,##0;0'
wb.save('../effects_matrix.xlsx')
```

### Implementing balance changes from a new spreadsheet version

When given an updated `effects_matrix.xlsx` with balance changes, follow these steps:

**1. Read the changed cells from the Policy Effects sheet**

For each changed cell, the row context tells you exactly where in `policy_constants.py` the change belongs:

| Row field | How to interpret |
|-----------|-----------------|
| Col A (Source Type) | `Policy Base` → `base` dict; `Policy Gov Mod` → `government_modifiers` dict; `Policy Trait Mod` → `trait_modifiers` dict |
| Col B (Name) | `{Category Name} -- {Level Name}` — parse category from `POLICY_CATEGORIES` by matching human name, parse level index by matching level name |
| Col D (Notes) | `base` (ignore); `when gov: {axis_value}` → key in `government_modifiers`; `when trait: {trait_key}` → key in `trait_modifiers` |

**2. Identify the effect key from the column number**

| Col | Effect key | Code value = cell value? |
|-----|-----------|--------------------------|
| 20 | `upkeep_reduction` | cell value (decimal, e.g. 0.04) |
| 31 | `stability_bonus` (if ≥ 0) or `stability_penalty` (if < 0) | cell value (flat number) |
| 32 | `growth_bonus` (if ≥ 0) or `growth_penalty` (if < 0) | cell value (decimal, e.g. 0.0005) |
| 33 | `integration_bonus` | cell value (decimal) |
| 35 | `research_bonus` (if ≥ 0) or `research_penalty` (if < 0) | cell value (decimal) |
| 38 | `food_production_bonus` | cell value (decimal) |
| 40 | `wealth_production_bonus` | cell value (decimal) |
| 42 | `manpower_bonus` | cell value (decimal, may be negative) |
| 43–65 | `building_efficiency_bonus[{category}]` | cell value (decimal) |
| 22,24,25,27,28,30 | military stub keys (see EFFECT_COL in export script) | cell value (decimal) |

**All cell values map directly to the code value** — no conversion needed. The spreadsheet stores 0.08, the code stores 0.08.

**3. Apply the change in `nations/policy_constants.py`**

Find the entry at `POLICY_EFFECTS[category_key][level_index]` and update the appropriate nested dict (`base`, `government_modifiers[axis_val]`, or `trait_modifiers[trait_key]`).

Category key format: lowercase with underscores (e.g. `"Military Service"` → `"military_service"`). Level index is the 0-based position in `POLICY_CATEGORIES[cat]["levels"]`.

**4. Regenerate the sheet to confirm round-trip**

Run `export_policy_effects.py` and verify the changed cell shows the new value.

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
DJANGO_SETTINGS_MODULE=phoenix_epoch.settings.dev ./venv/Scripts/python.exe -c "
import django; django.setup()
from economy.simulation import simulate_nation_economy
from economy.building_simulation import compute_building_efficiency, get_building_efficiency_modifiers
from provinces.jobs import get_province_job_status, calculate_province_designation
from provinces.models import AirZone, SeaZone, RiverZone
from provinces.travel import get_march_time, get_embark_time, get_zone_travel_time, check_cross_type_requirements
from provinces.travel_constants import CROSS_TYPE_REQUIREMENTS, FREE_CROSS_TYPE_TRANSITIONS
from nations.policy_effects import get_nation_policy_effects, validate_policy_change, get_policy_building_blocks, get_policy_unit_blocks
from nations.policy_constants import POLICY_EFFECTS, POLICY_REQUIREMENTS, POLICY_BANS, BUILDING_POLICY_REQUIREMENTS, BUILDING_POLICY_BANS, UNIT_POLICY_REQUIREMENTS, UNIT_POLICY_BANS
print('OK')
"
```

**Note:** `python` is intercepted by Windows Store on this machine. Always use `./venv/Scripts/python.exe` explicitly. `DJANGO_SETTINGS_MODULE=phoenix_epoch.settings.dev` must be set for every management command.

---

## Migrations status

| App | Migrations |
|-----|-----------|
| provinces | 0001_initial, 0002_add_province_designation, 0003_capital_designation_and_pop_default, 0004_*(military)*, 0005_zone_adjacency_and_travel |
| economy | 0001_initial, 0002_add_new_goods_to_nationgoodstock |
| nations | 0001_initial, 0002_ideology_traits_and_policies |
| All others | 0001_initial |

When adding model fields, always run `makemigrations <appname> --name descriptive_name`.
