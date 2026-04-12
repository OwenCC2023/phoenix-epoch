# Province Designations — Detailed Reference

> System 6 documentation. See `CLAUDE.md` for the system index.

## Key files

```
provinces/jobs.py        — calculate_province_designation()
provinces/constants.py   — DESIGNATION_SUBSISTENCE_MODIFIERS, DESIGNATION_BUILDING_MODIFIER, URBAN_THRESHOLD, URBAN_BUILDING_WEIGHT
```

---

### 6. Province designations

Computed each turn and persisted on `Province.designation`. Priority order:

1. **`capital`** — always, if `is_capital = True`. Government-building bonuses are a future stub.
2. **`urban`** — score ≥ threshold (standard: 100,000; urban_ruins: 40,000). Score = pop + active_buildings × 15,000. Requires sustained high growth AND investment.
3. **`post_urban`** — `urban_ruins` terrain below the urban threshold. Ruins of a former city; has a research/wealth lean.
4. **`rural`** — everything else. The default for the entire 30-year game for most provinces.

**Modifiers** (see `DESIGNATION_SUBSISTENCE_MODIFIERS` and `DESIGNATION_BUILDING_MODIFIER` in `provinces/constants.py`):

- Rural: +20% primary producers (food/materials/energy), −10% wealth/research
- Urban: −10–15% primary producers, +20% wealth/research, building output ×1.2
- Post-urban: moderate, +15% research, building output ×1.1
- Capital: similar to urban, +15% wealth/research, building output ×1.15

**Placement flags** dependent on designation: `urban_only` buildings (police_headquarters, police_station, disaster_management) require designation in `{"urban", "capital", "post_urban"}`; `rural_only` buildings (sheriffs_office) require `{"rural"}`. Enforced in `BuildingView.post`.
