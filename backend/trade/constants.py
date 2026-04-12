"""
Trade system constants.

Distance multipliers, speed, capacity weighting, and capital relocation costs.
"""

from provinces.constants import RELIEF_TYPES, VEGETATION_LEVELS, TEMPERATURE_BANDS

# ---------------------------------------------------------------------------
# Effective distance multipliers (pulled from province environment constants)
# ---------------------------------------------------------------------------
# These are re-exported here for convenience; the source of truth lives in
# provinces/constants.py (RELIEF_TYPES, VEGETATION_LEVELS, TEMPERATURE_BANDS).

RELIEF_TRADE_MULT = {k: v["trade_mult"] for k, v in RELIEF_TYPES.items()}
VEGETATION_TRADE_MULT = {k: v["trade_mult"] for k, v in VEGETATION_LEVELS.items()}
TEMPERATURE_TRADE_MULT = {k: v["trade_mult"] for k, v in TEMPERATURE_BANDS.items()}

# ---------------------------------------------------------------------------
# Trade speed
# ---------------------------------------------------------------------------
# Trade caravans/convoys move ~1.5x faster than marching armies because they
# follow established routes and don't need to maintain combat readiness.
from provinces.travel_constants import MARCH_SPEED

TRADE_SPEED_PER_TURN = MARCH_SPEED * 1.5  # 150.0 map units/turn

# Minimum arrival time — even adjacent capitals take at least 1 turn.
MIN_ARRIVAL_TURNS = 1

# ---------------------------------------------------------------------------
# Zone travel base costs for trade pathfinding (in map-unit equivalents)
# ---------------------------------------------------------------------------
# Sea/river/air zone hops are converted to a distance-equivalent so the
# Dijkstra graph uses a single comparable weight unit.
# These are the base distance-equivalent per hop before speed modifiers.
ZONE_HOP_DISTANCE = {
    "sea":   80.0,   # roughly one turn of trade travel
    "river": 60.0,   # rivers are faster than open sea for trade
    "air":   120.0,  # expensive but bypasses terrain
}

# Embark distance-equivalent (province <-> zone transition)
EMBARK_DISTANCE = {
    "sea":   20.0,
    "river": 10.0,
    "air":   30.0,
}

# ---------------------------------------------------------------------------
# Capacity
# ---------------------------------------------------------------------------
# Trade route capacity consumption = quantity × route_weight
# route_weight = total_length / CAPACITY_DISTANCE_NORMALISER
# This means a route of CAPACITY_DISTANCE_NORMALISER map-units costs
# exactly 1 capacity per unit of goods.
CAPACITY_DISTANCE_NORMALISER = 100.0

# ---------------------------------------------------------------------------
# Domain labels
# ---------------------------------------------------------------------------
TRADE_DOMAINS = ("land", "sea", "air")

# Mapping from domain to the building-effect key that provides capacity
DOMAIN_CAPACITY_EFFECT_KEY = {
    "land": "land_trade_capacity",
    "sea":  "naval_trade_capacity",
    "air":  "air_trade_capacity",
}

# ---------------------------------------------------------------------------
# Capital relocation
# ---------------------------------------------------------------------------
CAPITAL_MOVE_COST_WEALTH_PEACE = 500
CAPITAL_MOVE_COST_MATERIALS_PEACE = 200
CAPITAL_MOVE_DELAY_TURNS = 12

# Wartime (original capital held by enemy): half cost, instant
CAPITAL_MOVE_COST_WEALTH_WAR = CAPITAL_MOVE_COST_WEALTH_PEACE // 2
CAPITAL_MOVE_COST_MATERIALS_WAR = CAPITAL_MOVE_COST_MATERIALS_PEACE // 2
CAPITAL_MOVE_DELAY_TURNS_WAR = 0
