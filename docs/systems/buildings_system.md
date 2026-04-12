# Buildings System — Detailed Reference

> Systems 1, 1a–1e documentation. See `CLAUDE.md` for the system index.

## Key files

```
provinces/building_constants.py  — BUILDING_TYPES dict, per-level workers/inputs/outputs/costs/effects
economy/building_simulation.py   — building production, efficiency system, effect helpers
economy/simulation.py            — main turn loop (wires building output, trait effects)
nations/trait_constants.py       — 18 ideology traits, building_efficiency_bonus per trait
nations/government_constants.py  — get_combined_government_effects() for building_efficiency
nations/policy_constants.py      — POLICY_EFFECTS, BUILDING_POLICY_REQUIREMENTS, BUILDING_POLICY_BANS
nations/policy_effects.py        — get_nation_policy_effects(), get_policy_building_blocks()
```

---

### 1. Buildings system

**What:** Each province can have up to one building of each type. Buildings consume workers from the province population, consume input goods each turn, and produce output goods.

**75 building types** across 23 categories: `financial`, `light_manufacturing`, `heavy_manufacturing`, `refining`, `chemical`, `pharmaceutical`, `farming`, `extraction`, `construction`, `transport`, `communications`, `entertainment`, `healthcare`, `religious`, `green_energy`, `government_regulatory`, `government_oversight`, `government_management`, `government_security`, `government_education`, `government_organization`, `government_welfare`, `military_education`. Full building lists in `provinces/building_constants.py`.

**Why designed this way:** The production chain creates a bootstrapping problem — you can't run a factory without machinery, and you can't make machinery without a workshop. This mirrors real industrialisation and gives the game a natural progression arc.

**Key model:** `Building` (provinces app). Unique per (province, building_type). Has `level`, `is_active`, `under_construction`, `construction_turns_remaining`.

**Manufactured goods** tracked in `NationGoodStock`: `consumer_goods`, `arms`, `fuel`, `machinery`, `chemicals`, `medicine`, `components`, `heavy_equipment`. Basic resources produced by buildings (food, materials, energy, wealth, research) go to `NationResourcePool`.

**Use-it-or-lose-it effects:** `land_trade_capacity`, `naval_trade_capacity`, `air_trade_capacity`, and `bureaucratic_capacity` are computed fresh each turn from active buildings (summed nationally via `get_national_building_effects()`). They are NOT stockpiled. Financial buildings provide `land_trade_capacity` as a national effect. The old `trade_capacity` key has been split into three domain-specific keys.

**Building output formula:**
```
output = amount × effective_capacity × designation_mult × efficiency_mult
```
where `effective_capacity = min(worker_capacity_factor, input_goods_capacity)`.

---

### 1a. Building effects (province/national bonuses from buildings)

Each building level can declare an `effects` dict. Effect keys split into two scopes — full lists in `PROVINCE_EFFECT_KEYS` and `NATIONAL_EFFECT_KEYS` in `economy/building_simulation.py`.

Key province-scope effects: `security`, `farming_bonus`, `research_bonus`, `integration_bonus`, `growth_bonus`, `stability_recovery_bonus`, `construction_time_reduction`, `literacy_bonus`, transit speed modifiers.

Key national-scope effects: `upkeep_reduction`, `construction_cost_reduction`, `bureaucratic_capacity`, trade capacity (land/naval/air), transit speed modifiers, military stubs (training_speed, combat_bonus, upkeep_reduction per branch).

**Note on dual-scope keys:** `march_speed_bonus`, `sea_transit_speed`, `river_transit_speed`, and `air_transit_speed` appear in **both** scopes. Province-scope = that province's cross-type transitions only; national-scope = global same-type zone travel.

Helper functions: `get_province_building_effects(province)` and `get_national_building_effects(provinces)` in `economy/building_simulation.py`.

---

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

**Trait building_efficiency bonuses:** Several traits provide `building_efficiency_bonus` dicts in their effects. These are merged from the nation's 3 selected traits (1 strong + 2 weak, each with different magnitudes). See `nations/trait_constants.py` for the full definitions. Example traits with efficiency bonuses: militarist (heavy_manufacturing, chemical), positivist (communications, pharmaceutical), ecologist (farming, extraction, green_energy), industrialist (heavy_manufacturing, refining), spiritualist (religious, healthcare), etc.

**GM modifier usage:** Create a `NationModifier` with `category="building_efficiency"`, `target="chemical"` (any category) or `"all"`, `value=-0.25` (crisis) or `+0.20` (boon). Expiry via normal `expires_turn`.

**Co-location examples:**
- Workshop (needs `materials`) in a mountain province (produces materials) → +10%
- Factory (needs `materials`, `energy`, `machinery`) in a province with a workshop (which produces `machinery`) → +10% from supply-chain co-location
- Pharmaceutical lab (needs `chemicals`) in a province with a chemical plant → +10% from supply-chain co-location
- Co-location fires once regardless of how many inputs match.

**Cluster example:** Three chemical buildings in one province — each gets +2 × 5% = +10% cluster bonus.

---

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

---

### 1d. Ideology Traits system

**What:** Replaced the old single-ideology system. Each nation selects **3 traits from 3 different pairs** (9 pairs, 18 traits total): **1 strong trait** (full bonuses) + **2 weak traits** (reduced bonuses).

**Storage:** `Nation.ideology_traits` JSONField: `{"strong": "militarist", "weak": ["industrialist", "nationalist"]}`

**Key files:**
- `nations/trait_constants.py` — `TRAIT_PAIRS`, `TRAIT_DEFS`, `validate_trait_selection()`, `get_effective_trait_effects()`
- `nations/helpers.py` — `get_nation_trait_effects(nation)` merges strong+weak effects
- `economy/simulation.py` — wires trait effects into production, stability, growth, upkeep
- `economy/building_simulation.py` — trait `building_efficiency_bonus` is source 2 in efficiency system

**Trait effect types (wired into simulation):** `stability_bonus/penalty`, `growth_bonus/penalty`, `integration_bonus`, `research_bonus/penalty`, `manpower_bonus`, `wealth_production_bonus`, `food_production_bonus`, `upkeep_reduction`, `rural_output_bonus/penalty`, `urban_output_bonus` (stub), `urban_growth_penalty`, `urban_threshold_reduction`, `building_efficiency_bonus` (dict of category → bonus), `building_restrictions` (list of blocked building types).

**`security_multiplier`** is the one non-additive trait effect — merged multiplicatively, not additively. Honorable: 1.8/1.4 (strong/weak); Devious: 0.8/0.9. Handled by `_MULTIPLICATIVE_EFFECT_KEYS` in `trait_constants.py`.

**Stub effects (awaiting future systems):** trade_capacity, diplomatic_reputation, espionage, bureaucratic_capacity, military_organisation, etc. (`literacy` trait stub is now wired via System 11.)

---

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

**Legacy type → axis mapping:** `democracy→elections`, `autocracy→singular`, `junta→military_power`, `commune→collectivist`, `tribal→subsistence`, `theocracy→religious`, `corporate→liberal`.

**Effect keys wired into simulation:** `stability_bonus/penalty`, `growth_bonus/penalty`, `integration_bonus`, `research_bonus/penalty`, `manpower_bonus`, `wealth_production_bonus`, `food_production_bonus`, `upkeep_reduction`, `building_efficiency_bonus` (dict of category → bonus). Military keys (`army/navy/air_training_speed_bonus`, `*_upkeep_reduction`) are stubs.

**`POLICY_REQUIREMENTS`:** Gates policy level availability — `gov_axis_required/banned`, `traits_required/banned`, `policies_required`. **`POLICY_BANS`:** cross-policy incompatibilities. **`BUILDING_POLICY_REQUIREMENTS/BANS`:** `get_policy_building_blocks(nation)` → blocked building types (checked in `BuildingView.post`). **`UNIT_POLICY_REQUIREMENTS/BANS`:** `get_policy_unit_blocks(nation)` → blocked unit types (stub, wired when military sim built).
