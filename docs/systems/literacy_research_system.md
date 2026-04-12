# Literacy & Research System — Detailed Reference

> System 11 documentation. See `CLAUDE.md` for the system index.

## Key files

```
economy/literacy_constants.py    — S-curve growth parameters, policy penalties, happiness amplifier, migration sensitivity
economy/research_constants.py    — RESEARCH_UNLOCK_COSTS per sector, literacy-research multiplier constants
economy/literacy.py              — compute_literacy_growth(), get_national_literacy(), get_literacy_research_multiplier(),
                                   get_literacy_happiness_amplifier(), get_max_building_level()
economy/happiness.py             — compute_province_happiness() accepts literacy= param
economy/simulation.py            — Step 6a-bis: literacy growth; Step 7b: literacy research mult
economy/population.py            — literacy migration sensitivity in simulate_migration()
provinces/views.py               — BuildingView.post() checks get_max_building_level()
```

---

### 11. Literacy and Research System

**What:** `Province.literacy` — a 0.0–1.0 metric (fraction of literate population, starting at 0.20). Growth uses an S-curve formula (slowest at extremes, fastest near 50%). National average literacy multiplies research production and amplifies happiness deltas.

**Research unlocks:** Spending accumulated research unlocks higher building levels per sector. Base max level = 2 (L1-L2 always available). Tier 1 unlock (L3-L4) costs 3000–6000 research depending on sector. Tier 2 (L5-L6) costs 4× tier 1. Tracked in `ResearchUnlock` model.

**Literacy growth formula:**
```
S-curve base = BASE_LITERACY_GROWTH × lit × (1-lit) × 4
× (1 + literacy_bonus from buildings/traits)
× get_security_literacy_multiplier(security)     ← 0.7–1.2×
× (1 + min(wealth_per_cap / WEALTH_LITERACY_SCALE, WEALTH_LITERACY_CAP))
× (1 + CHILD_LABOR_LITERACY_PENALTY[level])
× (1 + SLAVERY_LITERACY_GROWTH_PENALTY[level])
capped by SLAVERY_LITERACY_CAP[level]
```

**Downstream effects (all live):**
| Effect | Formula |
|--------|---------|
| Research production | `× (0.3 + national_literacy × 1.0)` — at 20%: 0.5×, at 100%: 1.3× |
| Happiness delta amplification | `amplifier = 1.0 + literacy × 0.5` — at 100%: 1.5× |
| Starvation migration outflow | `× (1.0 + literacy × 0.3)` — at 100%: 30% more outflow |
| Building level gating | Levels > BASE_MAX_BUILDING_LEVEL (2) require a ResearchUnlock |

**Policy tie-ins wired:**
- `child_labor` levels 0–3: growth penalties 0%, -15%, -40%, -60%
- `slavery` levels 0–3: growth penalties 0%, -10%, -25%, -40%; literacy caps 100%, 90%, 70%, 50%

**Order type:** `research_unlock` — payload `{"sector": str, "tier": 1|2}`. Deducts research from pool, creates `ResearchUnlock` row. Executed before build orders each turn.

**API endpoint:** `GET /api/games/{game_id}/nations/{nation_id}/research/` — returns research pool, national literacy, unlocked sectors, available unlocks with costs.

**Building changes:** Madrasa `literacy_bonus` 0.10 → 0.06; Trading Post added `literacy_bonus: 0.02`.

**Migrations:** `provinces/migrations/0008_add_province_literacy.py`, `economy/migrations/0005_add_literacy_and_research_unlock.py`
