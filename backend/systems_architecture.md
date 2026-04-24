# Nation Simulation: Systems Architecture

## How everything connects

This document describes every system in the simulation, how they relate to each other, and the rules for extending any of them. Read this before adding anything new.

---

## 1. The five systems

There are five systems. Each operates at a different level of abstraction, and they layer on top of each other in a specific order.

```
TRAITS (cultural identity)
  ↓ disables certain →  GOV OPTIONS, POLICIES, BUILDINGS
  ↓ provides →          direct stat effects

GOV OPTIONS (government structure)
  ↓ disables certain →  POLICIES
  ↓ multiplies →        all POLICY effects (per-level multipliers)
  ↓ provides →          direct stat effects

POLICIES (laws and institutions)
  ↓ disable each other
  ↓ provides →          direct stat effects
  ↓ forbidden →         certain BUILDINGS

BUILDINGS (provincial infrastructure)
  ↓ provides →          direct stat effects (scaled by level)
```

### Evaluation order

When computing a nation's final stats:

1. **Traits** are chosen first (1 strong + 2 weak from 3 different pairs). Their direct effects apply. Their disabling rules remove options from Government, Policy, and Building pools.
2. **Government Options** are chosen (1 from each of 5 axes = 5 components). Their direct effects apply. Their disabling rules further restrict the Policy pool. Their multipliers scale all remaining Policy effects.
3. **Policies** are chosen (1 level per category from the 63 categories, minus any disabled by Traits or Gov). Their direct effects apply, multiplied by the Gov multiplier for that specific policy level. Policy-Policy disabling rules further restrict the pool (evaluated iteratively or at selection time). Some policies forbid specific Buildings.
4. **Buildings** are constructed in provinces from whatever remains in the allowed pool. Their effects apply at the provincial level, scaled by building level.

### The effect columns

All four systems write into the same set of effect columns. There are 162 columns total, organized into groups:

| Column range | Group | What it does | Who writes here |
|---|---|---|---|
| 2-14 | Province Effects | Per-province bonuses (stability recovery, growth, farming, research, integration, construction time, literacy, march/transit speed) | Buildings (primary), Policies, Traits |
| 15-20 | National Capacity | Nation-level caps and costs (trade capacity, bureaucratic capacity, upkeep, build cost) | Buildings, Policies, Gov Options |
| 21-29 | Military (stubs) | Army/Navy/Air training, combat, upkeep | Buildings (military), Policies, Traits |
| 28-39 | Gov & Trait Modifiers | Flat and percentage national modifiers (stability, growth, integration, trade, research, military, consumption, production by type) | Policies (primary), Traits, Gov Options |
| 40-62 | Building Efficiency | BE bonuses per building category | Gov Options, Traits (NOT policies or buildings) |
| 63-72 | Trait Effects | Manpower, kapital/food production, rural/urban modifiers | Traits (primary), Policies |
| 73-79 | Stubs | Training speed, mil upkeep, building restrictions, trade cap, espionage, diplomacy, arms production | Traits (primary), Policies |
| 80-158 | Building Forbidden | Binary: which buildings a policy forbids | Policies only |
| 159-161 | New Effects | Corruption Resistance, Environmental Health, Worker Productivity | Policies (primary), Traits |

**Key rule**: Buildings write to Provincial (2-14) and National Capacity (15-20) columns, with Military stubs (21-29) for military buildings and occasional Trait Effect columns (66, 82) for financial and arms buildings. Buildings do NOT write to Gov & Trait Modifiers (28-39) or Building Efficiency (40-62). Those are reserved for Policies, Gov Options, and Traits.

### How effects stack

From the Legend sheet:

- **Stability (flat) / Growth/turn**: Additive across all sources. A policy giving +0.5 stability and a trait giving +2 stability sum to +2.5.
- **Percentage modifiers** (Integration, Trade, Research, etc.): Additive from policies, but multiplicative between Gov/Trait sources and other sources.
- **Building Efficiency**: Gov components and Traits stack multiplicatively with each other. Other sources stack additively.
- **Building level scaling**: Base values shown are Level 1. Formula: `value × (1 + 0.9 × log₁₀(N))` for level N.

---

## 2. System details

### 2a. Buildings

**File**: `corrected_buildings_sheet.xlsx` (Corrected Buildings sheet)

79 buildings organized into categories: financial, light/heavy manufacturing, refining, chemical, pharmaceutical, farming, extraction, construction, transport, communications, entertainment, healthcare, religious, green energy, government (regulatory, oversight, management, security, education, organization, welfare), military education, military bases.

**Per building**: 2-4 effects, occasionally more for multi-function structures (Logistics Hub has 6). Effects should be concentrated in one column group (Provincial OR National Capacity OR Military), with at most 1-2 spillover effects into a second group.

**What buildings do NOT do**: Buildings do not set national policy. They don't modify stability (flat), integration (%), trade (%), or any other Gov/Trait modifier column. They provide concrete infrastructure: trade capacity in tonnes, stability recovery speed, construction time reduction, literacy from schools, growth from hospitals.

**Building Forbidden**: Policies can forbid specific buildings (cols 80-158 in the Policy Effects sheet). Traits can also forbid buildings (tracked in the Trait Disabling Rules sheet). A building is unavailable if ANY active policy or trait forbids it.

### 2b. Government Options

**Files**: `gov_policy_sheets.xlsx` (Gov-Policy Multipliers + Gov-Policy Disabling sheets), original `Government Options` sheet in the main workbook

5 axes, 1 choice per axis:

| Axis | Options |
|---|---|
| Direction | Top-Down, Bottom-Up |
| Economic Category | Liberal, Collectivist, Protectionist, Resource, Autarkic, Subsistence |
| Structure | Hereditary, Power-Consensus, Federal, Representative, Direct |
| Power Origin | Elections, Economic Success, Law & Order, Military Power, Religious, Ideology |
| Power Type | Singular, Council, Large Body, Multi-body, Staggered Groups |

**Direct effects**: Each gov option has its own stat effects (stored in the Government Options sheet in the main workbook). These use the same column layout as Traits and stack with them.

**Policy multipliers**: The Gov-Policy Multipliers sheet is a 24 × 277 matrix. Each cell contains a multiplier (default 1.0) that scales all effects of that specific policy level. Values >1.0 amplify, <1.0 dampen. The 5 chosen gov options each contribute a multiplier, and these multiply together. So if Top-Down gives Military Service: All Adults Serve a 1.4 and Military Power gives it a 1.4, the combined multiplier is 1.4 × 1.4 = 1.96, nearly doubling all that policy's effects.

**Gov-Policy Disabling**: 59 rules that make specific policy levels unavailable when specific gov options are chosen. These are hard blocks, not multiplier reductions.

### 2c. Traits (Ideology)

**File**: `trait_sheets.xlsx` (Traits Effects + Trait Disabling Rules sheets)

9 pairs of opposing traits. A nation picks 3 different pairs, then from those 3 pairs picks 1 strong and 2 weak (one strong from one pair, one weak from each of the other two). This means a nation always has exactly 3 traits: 1 strong, 2 weak.

| Pair | Trait A | Trait B |
|---|---|---|
| 0 | Internationalist | Nationalist |
| 1 | Spiritualist | Positivist |
| 2 | Libertarian | Authoritarian |
| 3 | Pacifist | Militarist |
| 4 | Devious | Honorable |
| 5 | Egalitarian | Elitist |
| 6 | Collectivist | Individualist |
| 7 | Industrialist | Ecologist |
| 8 | Modern | Traditionalist |

**Direct effects**: Strong versions have ~2x the magnitude of weak versions. Effects span the full column range including the 3 new columns (Corruption Resistance, Environmental Health, Worker Productivity).

**Trait Disabling Rules**: 125 rules across 3 target types:
- **Gov Option** (17 rules): A trait can make a government axis option unavailable. E.g., Strong Pacifist disables Military Power as a Power Origin.
- **Policy** (85 rules): A trait can make a specific policy level unavailable. E.g., Strong Libertarian disables Slavery: Common.
- **Building** (23 rules): A trait can forbid a building. E.g., Ecologist (both strong and weak) forbids Refinery, Oil Well, etc.

Strong traits disable more aggressively than weak traits. Some disabling rules apply even at weak strength (Ecologist always forbids oil infrastructure; Pacifist always forbids arms factories).

### 2d. Policies

**File**: `policy_effects_final.xlsx` (Corrected Policy Effects + Disabling Rules + New Effects Legend sheets)

63 categories, 277 total levels. A nation picks exactly 1 level per category.

**Direct effects**: 4-6 effects per level, with both positive and negative aspects on every level. Values write to the Gov & Trait Modifiers columns (28-39) primarily, plus Provincial effects, National Capacity, Trait Effects, stubs, Building Forbidden, and the 3 new columns.

**Policy-Policy Disabling**: 48 rules where one policy level makes another policy level unavailable. E.g., Unions: Illegal disables Minimum Wage: Collective Bargaining.

**Extremity gradient**: For ordinal policy categories (spectrums), levels at the extremes have stronger effects than levels in the middle. For distinct-type categories (like Bureaucracy), each level has a unique fingerprint with no gradient.

**Conditional categories**: Slavery Type is only meaningful when Slavery ≠ Illegal. All 5 Slavery Type levels are disabled when Slavery = Illegal.

### 2e. Effect columns

The 162 effect columns are the shared output space. Three were added during this work:

| Column | Name | Range | Description |
|---|---|---|---|
| 159 | Corruption Resistance | -0.06 to +0.05 | Institutional integrity. Fed by Bureaucracy, Policing, Anti-Corruption, Minimum Wage, Press Freedom, Suffrage, Consumer Protections, Gov Salary, Traits (Honorable, Devious, Positivist, etc.) |
| 160 | Environmental Health | -0.10 to +0.10 | Ecological condition. Fed by Conservation (primary), Resource Subsidies, Traits (Ecologist, Industrialist) |
| 161 | Worker Productivity | -0.03 to +0.03 | Per-worker efficiency. Fed by Minimum Wage, Working Hours, Holidays, Education, Health & Safety, Child Labor, Slavery, Unions, Traits (Egalitarian, Collectivist) |

---

## 3. The disabling cascade

Disabling rules flow in one direction: upstream systems disable downstream options.

```
Traits disable → Gov Options, Policies, Buildings
Gov Options disable → Policies
Policies disable → other Policies, Buildings
```

Nothing disables Traits. Nothing disables upstream. Policies cannot disable Gov Options. Buildings cannot disable anything.

When evaluating which options are available:
1. Start with all options open.
2. Apply Trait disabling rules (removes some Gov Options, Policies, Buildings).
3. Apply Gov Option disabling rules (removes some Policies).
4. Apply Policy-Policy disabling rules (removes some Policies based on other chosen Policies).
5. Apply Policy Building Forbidden rules (removes some Buildings).
6. Trait Building disabling rules also apply (already handled in step 2, but buildings are constructed later so the restriction persists).

---

## 4. How to add new things

### Adding a new Building

1. Pick a category from the existing list (financial, light_manufacturing, etc.) or define a new one.
2. Assign 2-4 effects using Provincial (cols 2-14) and National Capacity (cols 15-20) columns primarily. Military buildings can use Military stubs (cols 21-29). Financial buildings can use Kapital Prod (col 66). Arms-related buildings can use Arms Prod Bonus (col 82).
3. Do NOT assign effects in Gov & Trait Modifiers (28-39) or Building Efficiency (40-62). Those are for Policies, Gov Options, and Traits only.
4. Scale values to match existing buildings in the same category.
5. Check whether any existing Policy or Trait should forbid this building. Add disabling rules as needed.
6. If the building belongs to a new category, you may need to add a new Building Efficiency column (see "Adding a new effect column" below).

### Adding a new Trait

1. Traits come in opposing pairs. To add a new trait, add a whole new pair (Pair 9, etc.).
2. Define both Strong and Weak versions for both sides of the pair.
3. Strong versions should have ~2x the magnitude of Weak.
4. Each version gets 4-7 effects spanning the relevant column groups.
5. Define disabling rules for both Strong and Weak versions across all three target types (Gov Options, Policies, Buildings). Strong should disable more aggressively.
6. Check that the new pair doesn't redundantly cover the same thematic space as an existing pair. Each pair should represent a genuinely distinct cultural axis.
7. Ensure the new trait's disabling rules don't create impossible combinations (where picking 3 pairs leaves no valid gov/policy configurations).

### Adding a new Policy category

1. Define the category name and all its levels.
2. Classify it: ordinal spectrum, distinct types, tiered intensity, or binary.
3. Name the core tension.
4. Assign 4-6 effects per level using the domain mapping heuristics in plan.md.
5. Ensure every level has both positive and negative effects.
6. For ordinal categories, apply the extremity gradient.
7. Check for Policy-Policy disabling rules against all 63 existing categories.
8. Check if any existing Gov Option or Trait should disable any levels of this policy. Add rules to those disabling tables.
9. Check if any levels should forbid specific Buildings. Use Building Forbidden columns (80-158).
10. Update the Gov-Policy Multipliers matrix: add a new column for each new level and assign multipliers for all 24 gov options.
11. For new effect columns: at most 1 new column per 3 new categories, and it must be useful to multiple categories (see below).

### Adding a new Government Option

1. Gov Options belong to one of the 5 axes. A new option is added to an existing axis (e.g., a 7th Economic Category).
2. Define its direct stat effects using the same column layout as other gov options.
3. Add a new row to the Gov-Policy Multipliers matrix. Assign multipliers for all 277 policy levels (default 1.0, deviate where the gov option would amplify or dampen).
4. Define Gov-Policy disabling rules for any policy levels this option makes impossible.
5. Check whether any existing Trait should disable this option. Update the Trait Disabling Rules sheet.
6. Adding a new axis (a 6th government dimension) is a structural change. It requires a new row group in the Gov Options sheet, a new set of rows in the multiplier matrix, and a careful check that the combinatorial space doesn't explode. Avoid unless absolutely necessary.

### Adding a new effect column

New columns go at the end, after col 161 (Worker Productivity). Rules:

1. **Ratio limit**: At most 1 new column per 3 policy categories being worked on.
2. **Cross-system relevance**: The column must be useful to multiple systems. A column only relevant to one policy category is circular. Good examples: Corruption Resistance (fed by Bureaucracy, Policing, Anti-Corruption, Press, Suffrage, Gov Salary, Consumer Protections, Traits). Bad example: "Press Freedom" for the Freedom of Press category.
3. **No restating inputs**: The column must track a downstream consequence, not restate what a policy or trait IS.
4. **Define the scale**: Establish a numeric range consistent with existing columns. Document it in the New Effects Legend sheet.
5. **Update all systems**: A new column should receive values from the relevant policies, traits, and potentially gov options. Buildings generally do not write to new effect columns unless they represent concrete infrastructure output.
6. **Document**: Add an entry to the New Effects Legend sheet explaining the column's purpose, scale, and which systems feed it.

### Adding a new system

A new system (e.g., "Diplomatic Stances," "Religious Doctrine," "Economic Era") requires:

1. **Define its relationship to existing systems**: Where does it sit in the evaluation order? What does it disable? What multiplies it?
2. **Define its output**: Does it write to existing effect columns, or does it need new ones?
3. **Define its input constraints**: What disables its options? Traits? Gov? Other systems?
4. **Define its interaction with Policies**: Does it multiply policy effects (like Gov Options do)? Does it provide flat effects (like Traits)? Both?
5. **Update this document** with the new system's position in the architecture.

The most likely new system would be something like "Era" or "Technology Level" that gates which buildings, policies, or gov options are available based on a progression mechanic. This would add a new disabling layer that sits above or alongside Traits in the cascade.

---

## 5. Scale reference

All numeric values across all systems should be internally consistent. These ranges were established during this work and should be maintained.

### Provincial effects (buildings, some policies)
| Effect | Typical range | Notes |
|---|---|---|
| Stability Recovery/turn | 0.05 - 0.20 | Per building, additive |
| Growth/turn | 0.001 - 0.003 | Very small, compounds |
| Farming Bonus | 0.05 - 0.15 | Per building |
| Research Bonus | 0.05 - 0.15 | Per building |
| Integration Bonus | 0.03 - 0.08 | Per building |
| Construction Time | 0.03 - 0.10 | Per building (negative = faster) |
| Literacy Bonus | 0.03 - 0.10 | Per building |
| March Speed | 0.02 - 0.15 | Per building |
| Transit (sea/river/air) | 0.02 - 0.25 | Per building, varies by type |

### National capacity (buildings, policies)
| Effect | Typical range | Notes |
|---|---|---|
| Trade Capacity (land/naval/air) | 5 - 240 | Absolute units, varies wildly by building type |
| Bureaucratic Capacity | 5 - 30 | Absolute units |
| Upkeep reduction | 0.01 - 0.04 | Percentage per source |
| Build Cost reduction | 0.02 - 0.05 | Percentage per source |

### Gov & Trait Modifiers (policies, traits, gov options)
| Effect | Range (policies) | Range (traits) |
|---|---|---|
| Stability (flat) | -1.5 to +1.5 | -3 to +4 |
| Growth/turn | -0.06 to +0.06 | -0.001 to +0.002 |
| Integration (%) | -0.06 to +0.06 | -0.05 to +0.06 |
| Trade (%) | -0.04 to +0.04 | -0.15 to +0.10 |
| Research (%) | -0.04 to +0.05 | -0.10 to +0.15 (as bonus) |
| Military (%) | -0.06 to +0.06 | 0 to +0.10 |
| Consumption (%) | -0.05 to +0.04 | n/a |
| Production (food/materials/kapital/energy/manpower) | -0.06 to +0.06 | -0.05 to +0.15 |

### Building Efficiency (gov options, traits only)
| Range | Notes |
|---|---|
| 0.04 to 0.15 | Per gov/trait source, multiplicative between sources |

### New columns
| Column | Range | Primary sources |
|---|---|---|
| Corruption Resistance | -0.06 to +0.05 | Policies, Traits |
| Environmental Health | -0.10 to +0.10 | Policies (Conservation), Traits (Ecologist/Industrialist) |
| Worker Productivity | -0.03 to +0.03 | Policies, Traits |

### Gov-Policy Multipliers
| Range | Meaning |
|---|---|
| 0.2 - 0.5 | Strongly dampened (near-incompatible) |
| 0.6 - 0.8 | Moderately dampened |
| 1.0 | Default (no modification) |
| 1.2 - 1.3 | Moderately amplified |
| 1.4 - 1.5 | Strongly amplified |

---

## 6. File inventory

| File | Sheets | Purpose |
|---|---|---|
| `corrected_effects_matrix.xlsx` | Buildings, Corrected Buildings, Government Options, Traits, Policy Effects, Corrected Policy Effects, Legend | Master workbook. The "Corrected" sheets are the active ones. |
| `policy_effects_final.xlsx` | Corrected Policy Effects, Disabling Rules, New Effects Legend | Full policy effects matrix (63 categories, 277 levels, 162 columns) + policy-policy disabling rules + documentation of new columns. Drop this into the master workbook. |
| `gov_policy_sheets.xlsx` | Gov-Policy Multipliers, Gov-Policy Disabling | 24×277 multiplier matrix + 59 gov-policy disabling rules. Add as new sheets. |
| `trait_sheets.xlsx` | Traits Effects, Trait Disabling Rules | Reworked traits (36 rows) + 125 disabling rules across Gov/Policy/Building. Replaces the Traits sheet. |
| `corrected_buildings_sheet.xlsx` | Corrected Buildings | Reworked buildings (79 buildings, 183 effects). Replaces the Corrected Buildings sheet. |
| `plan.md` | n/a | Detailed heuristics for assigning policy effects. Reference for future instances filling in policy data. |

---

## 7. Common mistakes to avoid

1. **Buildings writing to policy columns.** A hospital does not modify national stability (flat) or integration (%). It provides growth/turn and stability recovery/turn at the provincial level. Keep buildings concrete.

2. **Policies restating themselves.** A "Press Freedom" column for the Freedom of Press policy is circular. The effects of press freedom should appear as changes to research, stability, corruption resistance, entertainment BE, etc.

3. **Symmetric extremes on asymmetric spectrums.** "Closed Borders" and "No Borders" are not mirror images. One is the status quo plus a wall; the other is a radical dissolution. Let the logic drive asymmetry.

4. **Overloading stability.** If every policy touches Stability (flat), the stacking becomes absurd. Spread effects across the full column set. Currently 261 of 277 policy levels write to Stability, which is already high. Favor other columns when the policy's primary impact isn't really about stability.

5. **Forgetting the negative.** Every policy level needs both positive and negative effects. No free lunches. Even "Illegal Slavery" has a small negative (slightly less raw manpower from forced labor).

6. **New columns that only serve one category.** The 1-per-3 ratio exists for a reason. If a column is only written to by the category that inspired it, it adds a dimension of complexity with no cross-system interplay. Cut it.

7. **Disabling rules that create dead ends.** Before adding a disabling rule, check that the combination of Traits + Gov + existing disabling rules still leaves at least one valid option in every policy category. A nation must always be able to pick something.

8. **Gov multipliers below 0.3 or above 1.5.** The multipliers compound across 5 gov axes. If three axes each give a 1.5× to the same policy level, that's 1.5³ = 3.375×, which triples the policy's effects. Keep individual multipliers moderate.
