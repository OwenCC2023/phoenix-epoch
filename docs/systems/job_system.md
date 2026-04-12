# Job System — Detailed Reference

> System 5 documentation. See `CLAUDE.md` for the system index.

## Key files

```
provinces/jobs.py           — get_province_job_status(), _JOB_CAPACITY_PROVIDERS registry
provinces/constants.py      — SUBSISTENCE_RATE, terrain definitions
economy/building_simulation.py — worker_capacity_factor used in building output
```

---

### 5. Job system

Two tiers of employment per province:

- **Subsistence**: all workers not in buildings. Produce the terrain's *primary resource* at `SUBSISTENCE_RATE × terrain_best_multiplier`. Deliberately low productivity.
- **Building jobs**: each active completed building provides `workers` slots. Workers fill building slots before doing subsistence. Partial staffing → `worker_capacity_factor < 1.0` → buildings operate at reduced output.

Extensible via `_JOB_CAPACITY_PROVIDERS` registry in `provinces/jobs.py`.
