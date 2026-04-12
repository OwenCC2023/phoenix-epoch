# Travel & Zone System — Detailed Reference

> System 7 documentation. See `CLAUDE.md` for the system index.

## Key files

```
provinces/travel_constants.py  — MARCH_SPEED, EMBARK_SPEED, BASE_ZONE_TRAVEL, FREE_CROSS_TYPE_TRANSITIONS,
                                  CROSS_TYPE_REQUIREMENTS (OR-group structure), speed modifier key maps
provinces/travel.py            — get_march_time(), get_embark_time(), get_zone_travel_time(),
                                  check_cross_type_requirements()
provinces/models.py            — AirZone, SeaZone, RiverZone models (defined before Province)
```

---

### 7. Province zone adjacency & travel time system

**What:** Provinces now have a geographic graph. Three zone types exist alongside province-to-province adjacency. Travel time functions underpin the future combat and trade systems.

**Three zone models** (in `provinces/models.py`, before `Province`):
- `AirZone` — game-scoped; self-referential M2M adjacency
- `SeaZone` — game-scoped; M2M to other SeaZones and to AirZones; reverse FK from RiverZone
- `RiverZone` — game-scoped; FK to SeaZone (which sea it drains to); M2M to other RiverZones and AirZones

**Province fields added:**
- `center_x`, `center_y` — abstract map coordinates (nullable until map is developed)
- `sea_border_distance`, `river_border_distance` — distance from center to the relevant border edge (nullable)
- `air_zone` — FK to AirZone (SET_NULL)
- `adjacent_provinces` — symmetrical M2M self-referential
- `adjacent_sea_zones` — M2M to SeaZone
- `adjacent_river_zones` — M2M to RiverZone

**Travel time formulas:**
- Province→Province: `distance(centers) / (MARCH_SPEED × (1 + march_speed_bonus))` — falls back to `DEFAULT_MARCH_TIME = 1.0` when coordinates are null
- Province↔Sea/River: `border_distance / (EMBARK_SPEED × (1 + transit_speed_bonus))` — falls back to `DEFAULT_EMBARK_TIME = 0.1`; with `EMBARK_SPEED = 1000` and typical distances of 5–20 map units this gives 0.005–0.02 turns
- Zone→Zone (same type): `BASE_ZONE_TRAVEL[type] / (1 + zone_speed_bonus)` — base is 1.0 turn for all three types
- Free (zero-cost) transitions: sea↔air, river↔air

**Cross-type requirements:** `CROSS_TYPE_REQUIREMENTS` uses an OR-group structure (`list[list[str]]`). Province↔sea requires `dock`. Province↔air requires `air_base` **or** `airport`. Province↔river has no requirement.

**Transport building placement restrictions** (enforced in `BuildingView.post`):
- `dock`, `port` — coastal provinces only
- `bridge` — river provinces only

**Transport buildings** (dock, port, bridge, railroad, train_depot, train_station, train_cargo_terminal, airport, air_cargo_terminal) provide province-scope or national-scope transit speed and trade capacity effects. Full effect mapping in `provinces/building_constants.py`.

**API endpoints** (under `/api/games/{game_id}/provinces/`):
- `GET zones/air/` → AirZoneListView
- `GET zones/sea/` → SeaZoneListView
- `GET zones/river/` → RiverZoneListView

Serializers return adjacency as ID lists (not nested) to avoid recursive graph serialisation.

**Admin:** All three zone types registered with `filter_horizontal` for M2M adjacency management. `ProvinceAdmin` updated with `air_zone` display and M2M adjacency filter widgets.
