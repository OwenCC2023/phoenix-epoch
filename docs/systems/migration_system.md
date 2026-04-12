# Migration System — Detailed Reference

> System 4 documentation. See `CLAUDE.md` for the system index.

## Key files

```
economy/population.py   — simulate_migration(), simulate_economic_migration()
economy/constants.py    — MIGRATION_RATE, ECONOMIC_MIGRATION_RATE
economy/happiness.py    — happiness weight used in migration destination scoring
economy/security.py     — security weight used in migration destination scoring
```

---

### 4. Migration — two processes

**Starvation migration** (`simulate_migration`): provinces with negative growth rate lose population proportional to `|rate| × MIGRATION_RATE`. If any province is growing → internal (national total conserved). If *all* provinces are declining → external (migrants leave the nation; national total shrinks).

**Economic migration** (`simulate_economic_migration`): subsistence workers in provinces with no unfilled building jobs migrate to provinces with unfilled building slots, *if* the destination is not declining. Always internal. Rate = `ECONOMIC_MIGRATION_RATE = 0.02` (per month).

**Migration destination weighting** (both processes): destination provinces are weighted by `happiness_mult × security_mult` (where mult = `local_happiness / 50` or `local_security / 50`, floored at 0.1). Unhappy or insecure provinces attract proportionally fewer migrants.

**Literacy sensitivity:** Starvation migration outflow is multiplied by `(1.0 + literacy × 0.3)` — at 100% literacy, 30% more population flees starvation. See `docs/systems/literacy_research_system.md`.
