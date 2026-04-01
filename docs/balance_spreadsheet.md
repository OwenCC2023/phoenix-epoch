# Balance Spreadsheet Reference — effects_matrix.xlsx

`effects_matrix.xlsx` in the repo root is the authoritative balance reference.

## Sheets

| Sheet | Content |
|-------|---------|
| Buildings | Per-building, per-level effects at L1 (all 75 buildings) |
| Government Options | Per-axis-value effects for the five government axes |
| Traits | Per-trait effects (strong and weak rows separate) |
| Policy Effects | Per-policy-level effects (base, gov modifier, trait modifier rows) |
| Legend | Colour key and scale notes |

All numeric cells are real numbers (not text). Percentages are stored as decimals (0.08 = 8%) with a `+0.0%;-0.0%` format. Flat values use `+0.0;-0.0` or integer format. Cell colours: green = positive wired effect, red = negative wired effect, yellow = stub (declared but not yet wired), blue row = first entry in a new category group.

## Column layout (all sheets share this structure)

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

## Policy Effects sheet row structure

Each row represents one effect source for one policy level:

| Col | Content |
|-----|---------|
| A (Source Type) | `Policy Base` / `Policy Gov Mod` / `Policy Trait Mod` |
| B (Name) | `{Category Name} -- {Level Name}` |
| C (Category) | Policy category name (human-readable) |
| D (Notes) | `base` \| `when gov: {axis_value}` \| `when trait: {trait_key}` |
| E–CF | Effect values |

Rows with no effects are omitted. First row of each policy category is blue; subsequent rows for the same category are light gray.

## Regenerating the Policy Effects sheet

```bash
cd backend
DJANGO_SETTINGS_MODULE=phoenix_epoch.settings.dev ./venv/Scripts/python.exe ../tools/export_policy_effects.py
```

`tools/export_policy_effects.py` reads `POLICY_CATEGORIES` and `POLICY_EFFECTS` from `nations/policy_constants.py` and rewrites only the Policy Effects sheet, leaving the other sheets untouched.

## Implementing balance changes from a new spreadsheet version

### 1. Read the changed cells from the Policy Effects sheet

| Row field | How to interpret |
|-----------|-----------------|
| Col A (Source Type) | `Policy Base` → `base` dict; `Policy Gov Mod` → `government_modifiers` dict; `Policy Trait Mod` → `trait_modifiers` dict |
| Col B (Name) | `{Category Name} -- {Level Name}` — parse category from `POLICY_CATEGORIES` by matching human name, parse level index by matching level name |
| Col D (Notes) | `base` (ignore); `when gov: {axis_value}` → key in `government_modifiers`; `when trait: {trait_key}` → key in `trait_modifiers` |

### 2. Identify the effect key from the column number

| Col | Effect key | Notes |
|-----|-----------|-------|
| 20 | `upkeep_reduction` | decimal, e.g. 0.04 |
| 31 | `stability_bonus` (if ≥ 0) or `stability_penalty` (if < 0) | flat number |
| 32 | `growth_bonus` (if ≥ 0) or `growth_penalty` (if < 0) | decimal, e.g. 0.0005 |
| 33 | `integration_bonus` | decimal |
| 35 | `research_bonus` (if ≥ 0) or `research_penalty` (if < 0) | decimal |
| 38 | `food_production_bonus` | decimal |
| 40 | `wealth_production_bonus` | decimal |
| 42 | `manpower_bonus` | decimal, may be negative |
| 43–65 | `building_efficiency_bonus[{category}]` | decimal |
| 22,24,25,27,28,30 | military stub keys (see EFFECT_COL in export script) | decimal |

All cell values map directly to the code value — no conversion needed. The spreadsheet stores 0.08, the code stores 0.08.

### 3. Apply the change in `nations/policy_constants.py`

Find the entry at `POLICY_EFFECTS[category_key][level_index]` and update the appropriate nested dict (`base`, `government_modifiers[axis_val]`, or `trait_modifiers[trait_key]`).

Category key format: lowercase with underscores (e.g. `"Military Service"` → `"military_service"`). Level index is the 0-based position in `POLICY_CATEGORIES[cat]["levels"]`.

### 4. Regenerate the sheet to confirm round-trip

Run `export_policy_effects.py` and verify the changed cell shows the new value.
