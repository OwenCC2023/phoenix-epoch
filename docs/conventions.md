# Codebase Conventions

> Cross-cutting development conventions. See `CLAUDE.md` for the project index.

## Circular imports

Broken with lazy imports inside functions, not at module level. Follow this pattern when a new `nations/` module needs to call back into `policy_effects.py` or `economy/building_simulation.py`. See `nations/bureaucratic_capacity.py` for a working example.

## New systems

Add a constants file + logic module pair (e.g. `bureaucratic_constants.py` + `bureaucratic_capacity.py`). Wire into:
- `policy_effects.validate_policy_change()` for change-time gates
- `economy/simulation.simulate_nation_economy()` for per-turn effects (owned provinces)
- `economy/simulation.simulate_economy_for_game()` for game-wide effects (e.g. unclaimed province loops)

Document in `docs/systems/` following the existing format (key files table, field descriptions, formulas, tie-ins table).

## Constants files

Pure Python — dicts, frozensets, and numeric constants only. No imports from Django or other app modules. Helper functions for computed lookups are fine (e.g. `get_consuming_tier_count()`). Use section headers with `# ---` dividers. See `nations/bureaucratic_constants.py` for the pattern.

## Migrations

Always run `makemigrations <appname> --name descriptive_name` when adding model fields. Update the migrations status table in `CLAUDE.md` after each new migration.

## Simulation multiplier stacking

Building output formula in `economy/building_simulation.py`:

```
produce = amount × effective_capacity × designation_mult × efficiency_mult × productivity_mult
```

- `efficiency_mult` combines gov/traits/GM modifiers + colocation + concentration (all additive-then-multiplicative)
- **Development Points (System 17)** apply as a final multiplicative layer *after* `produce` is computed — a true multiplier of multipliers. Integration point: `economy/building_simulation.py` after the `produce` line, inside the `output_goods` loop.
- Subsistence DP applied in `economy/simulation.py` Step 3, after all other subsistence modifiers.
