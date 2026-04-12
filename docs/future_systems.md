# Future Systems & Stub Reference

> Unbuilt systems and declared-but-unwired effect keys. See `CLAUDE.md` for the system index.

## Military system
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

## Bureaucratic capacity
The `capital` designation is a stub. Once built, government buildings in the capital should provide bureaucratic capacity that enables larger nations (higher integration efficiency, more provinces before administrative penalties, etc.).

## Events system
`GameEvent` model and `events/helpers.py` exist. GM-created events can apply national modifiers. Not yet integrated into turn resolution loop.

## Province control / conquest
**Economic acquisition and espionage persuasion (System 12) are implemented.** Military conquest, diplomatic acquisition, and the full combat system are not yet built. Provinces can be reassigned via admin for testing.

## Construction cost/time reduction (wiring stub)
`construction_cost_reduction` (national) and `construction_time_reduction` (province) effects are computed by buildings but not yet applied in the build API. `get_construction_modifiers(nation)` in `building_simulation.py` aggregates cost reduction and is ready to call from the construction view.

---

## Stub effect keys (declared but not wired)

**Building/province scope:**
- `literacy_bonus` — **now wired**: drives `compute_literacy_growth()` in `economy/literacy.py`
- `construction_time_reduction` — fraction reduction in construction turns (computed by `get_construction_modifiers()` but not applied in build API)

**National scope:**
- `construction_cost_reduction` — computed by `get_construction_modifiers()` but not applied in build API
- `bureaucratic_capacity` — use-it-or-lose-it capacity system (declared in `NATIONAL_EFFECT_KEYS`)
- `army_training_speed_bonus`, `navy_training_speed_bonus`, `air_training_speed_bonus` — wired in skeleton when military simulation built
- `army_combat_bonus`, `navy_combat_bonus`, `air_combat_bonus` — wired when combat system built
- `army_upkeep_reduction`, `navy_upkeep_reduction`, `air_upkeep_reduction` — wired when military upkeep system built

**Trait scope:**
- `urban_output_bonus` — building output multiplier in urban provinces (stub — not yet wired in `building_simulation.py`)
- `trade_capacity` — diplomatic/internal trade bonuses (note: `trade_pct` and `trade_capacity_bonus/penalty` are wired; this stub covers future diplomatic trade effects)
- `diplomatic_reputation` — reputation modifiers
- `espionage` — espionage effectiveness
- `literacy` — **now wired** via System 11: `get_literacy_research_multiplier()` and happiness amplifier
- `military_organisation` — military structural efficiency

**Policy/Unit gates:**
- `UNIT_POLICY_REQUIREMENTS` / `UNIT_POLICY_BANS` — unit type blocking by policy (gate stubs, awaiting military unit system)
