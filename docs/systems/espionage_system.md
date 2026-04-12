# Espionage System — Detailed Reference

> System 10 documentation. See `CLAUDE.md` for the system index.

## Key files

```
espionage/constants.py      — espionage balance: policy/trait modifiers, stability/literacy breakpoints, action defs
espionage/computation.py    — compute_national_attack(), compute_national_defense(), compute_transparency()
espionage/revelation.py     — compute_revealed_info(), transparency category weights
espionage/simulation.py     — simulate_espionage() per-turn loop, called from turns/engine.py after economy
espionage/action_effects.py — apply_promote_foreign_ideology(), apply_terrorist_attack(), apply_sabotage_building()
espionage/slots.py          — slot capacity helpers (foreign targets, action types, suppress)
espionage/models.py         — EspionageState, EspionageAction, IntelligenceSharing, BranchOfficeSpecialization
```

---

### 10. Espionage system

**What:** Inter-nation espionage with Attack vs Defense dynamics, a Transparency information revelation system, and 5 espionage action types. Each turn, for every (attacker, target) nation pair, the system computes attack, defense, transparency (0.0–1.0), and determines what information is revealed.

**Models** (`espionage/models.py`):
- `EspionageState` — per (attacker, target) pair: national_attack, national_defense, transparency, revealed_info JSON, turn_updated
- `EspionageAction` — tracks active/completed operations: 5 action types (investigate_province, promote_foreign_ideology, terrorist_attack, sabotage_building, suppress_foreign_operations), status lifecycle (active → completed/failed/cancelled)
- `IntelligenceSharing` — voluntary per-category sharing toggles between nations (5 categories)
- `BranchOfficeSpecialization` — links a branch_office Building to a foreign action type (OneToOne)

**Attack formula:**
```
If FIA policy level == 0: attack = 0 (hard gate)
base = building_espionage_attack + FIA_policy_modifier + trait_attack_modifiers
effective = base × (1.0 + espionage_bonus) + stability_breakpoint_bonus
```

**Defense formula:**
```
base = building_espionage_defense + Σ(10 policy defense modifiers) + trait_defense_modifiers
effective = base × (1.0 + counter_espionage_bonus) + stability_bonus + literacy_bonus
```

**Transparency:** `min(1.0, (attack - defense) / defense)` — 0 if attack ≤ defense; 1.0 if defense ≤ 0 and attack > 0.

**Provincial defense:** `national_defense + local_office_effects + suppress_bonus(15)`

**Policy defense modifiers** (10 categories in `espionage/constants.py: ESPIONAGE_DEFENSE_POLICY_MODIFIERS`):
policing, anti_corruption_policy, visa_policy, naturalization_laws, domestic_intelligence_agency, freedom_of_movement, freedom_of_association, gender_rights, racial_rights, social_discrimination.

**Attack policy modifier:** Only `foreign_intelligence_agency` — level 0 = hard gate (zero attack), levels 1/2/3 = +5/+10/+18.

**Trait modifiers** (`ESPIONAGE_TRAIT_MODIFIERS`): authoritarian (+6/+3 def), honorable (+8/+4 def), devious (+10/+5 atk, -6/-3 def), libertarian (-6/-3 def).

**Stability breakpoints** (relative advantage): +5→+2, +10→+4, +20→+7, +30→+10 (same for attack and defense).

**Literacy breakpoints** (defense only, stub): +5→+2, +10→+4, +20→+6.

**Information revelation** (`espionage/revelation.py`): 5 categories ordered easiest→hardest with weights:
| Category | Weight | Content |
|----------|--------|---------|
| building_locations | 0.30 | Buildings per province |
| province_level_info | 0.25 | Stability, happiness, security, population, wealth |
| positions_of_formations | 0.20 | Military formations (stub) |
| cointel | 0.15 | Provinces with active suppress_foreign_operations |
| foreign_espionage | 0.10 | Nations being targeted by target's foreign actions |

Within categories, most populous provinces are revealed first. `foreign_espionage` uses whole-increment random selection. Voluntary shares (`IntelligenceSharing`) override to 100% for that category.

**Espionage actions:**
| Action | Type | Min FIA/DIA | Duration | Effect |
|--------|------|-------------|----------|--------|
| investigate_province | foreign | FIA ≥ 1 | 1 turn | +30 attack bonus for per-province transparency |
| promote_foreign_ideology | foreign | FIA ≥ 1 | 3 turns | stability −2×(1+transparency)/turn, security −1/turn; extra −1.5 stability if happiness<40 or security<30 |
| terrorist_attack | foreign | FIA ≥ 2 | 1 turn | Kill ceil(pop×0.002), security −20 penalty for 3 turns (NationModifier) |
| sabotage_building | foreign | FIA ≥ 2 | 1 turn | Disable building for max(1, round(2+3×transparency)) turns |
| suppress_foreign_operations | domestic | DIA ≥ 1 | persistent | +15 provincial defense in target province |

**Slot system** (`espionage/slots.py`):
- Foreign target slots = `foreign_intel_hq.level` (max simultaneous foreign nations)
- Per-action-type slots = sum of `branch_office` levels with matching specialization
- Suppress slots = `domestic_intel_hq.level`

**Espionage buildings** (4 new, in `provinces/building_constants.py`):
| Building | Scope | Key Effect | Unique |
|----------|-------|-----------|--------|
| foreign_intel_hq | national | espionage_attack: 8 | per-nation |
| branch_office | national | espionage_attack: 3 | no |
| domestic_intel_hq | national | espionage_defense: 8 | per-nation |
| local_office | province | provincial_espionage_defense: 5 | no |

Building policy requirements: foreign_intel_hq & branch_office require FIA ≥ 1; domestic_intel_hq requires DIA ≥ 1.

**Order types:** `espionage_action`, `specialize_branch_office` — validated in `turns/validators.py`, executed in `turns/engine.py: _execute_espionage_orders()`.

**Turn integration:** `simulate_espionage(game, turn_number)` runs after economy simulation. Computes all pairs, applies action effects, expires completed actions, re-enables sabotaged buildings.

**API endpoints** (under `/api/games/<game_id>/espionage/`):
- `GET overview/` — attack/defense/transparency per target
- `GET targets/<target_nation_id>/` — revealed_info for specific target
- `GET/POST sharing/` — voluntary intelligence sharing toggles
- `GET actions/` — active espionage actions
- `GET slots/` — available/used slot capacity

**Security constraint:** Nations can only see their OWN attack/transparency and info revealed TO them.

**Effect keys added:**
- National: `espionage_attack`, `espionage_defense`
- Province: `provincial_espionage_defense`

**Existing stub keys wired:** `espionage_bonus` (multiplicative attack scaler), `counter_espionage_bonus` (multiplicative defense scaler) — already emitted by Devious trait and FIA/DIA policies.
