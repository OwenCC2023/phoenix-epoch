# Construction System — Detailed Reference

> System 2 documentation. See `CLAUDE.md` for the system index.

## Key files

```
economy/construction.py          — construction tick, completion
economy/building_simulation.py   — get_construction_modifiers(nation)
provinces/views.py               — BuildingView.post() (build order entry point)
```

---

### 2. Construction system

Buildings have a construction cost (paid immediately from `NationResourcePool`) and a `construction_turns` countdown. Each turn `process_construction_tick()` advances all under-construction buildings. The player can queue one building upgrade per province at a time. `get_nation_under_construction()` provides the construction queue for the UI.

`get_construction_modifiers(nation)` in `building_simulation.py` aggregates the national `construction_cost_reduction` from active buildings — ready to wire into the build API when needed.

**Stub:** `construction_cost_reduction` (national) and `construction_time_reduction` (province) effects are computed but not yet applied in the build API. See `docs/future_systems.md` for details.
