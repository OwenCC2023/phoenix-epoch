"""Terrain types and their base production multipliers."""

# ---------------------------------------------------------------------------
# Trade-related province environment constants
# ---------------------------------------------------------------------------

# Relief axis: determines terrain friction for trade distance calculation.
# Separate from terrain_type (biome) — a forest can be flat or mountainous.
RELIEF_TYPES = {
    "flat":        {"label": "Flat",        "trade_mult": 1.00},
    "hilly":       {"label": "Hilly",       "trade_mult": 1.15},
    "rugged":      {"label": "Rugged",      "trade_mult": 1.25},
    "marshy":      {"label": "Marshy",      "trade_mult": 1.35},
    "mountainous": {"label": "Mountainous", "trade_mult": 1.60},
}

VEGETATION_LEVELS = {
    "none":   {"label": "None",   "trade_mult": 0.95},
    "low":    {"label": "Low",    "trade_mult": 1.00},
    "medium": {"label": "Medium", "trade_mult": 1.15},
    "high":   {"label": "High",   "trade_mult": 1.35},
}

TEMPERATURE_BANDS = {
    "mild": {"label": "Mild", "trade_mult": 1.00},
    "hot":  {"label": "Hot",  "trade_mult": 1.10},
    "cold": {"label": "Cold", "trade_mult": 1.15},
}

# Mapping from existing biome terrain_type to default relief value.
# Used only by the data migration to seed Province.relief.
TERRAIN_TYPE_TO_RELIEF = {
    "plains":      "flat",
    "mountains":   "mountainous",
    "forest":      "rugged",
    "coast":       "flat",
    "desert":      "flat",
    "urban_ruins": "flat",
    "wasteland":   "rugged",
    "river_valley": "marshy",
}

# Each terrain defines multipliers for sector production rates.
# A multiplier of 1.0 is baseline. Higher = better for that sector.
TERRAIN_TYPES = {
    "plains": {
        "label": "Plains",
        "description": "Flat fertile land, excellent for farming.",
        "multipliers": {
            "agriculture": 1.5,
            "industry": 0.8,
            "energy": 0.9,
            "commerce": 1.0,
            "military": 1.0,
            "research": 0.8,
        },
    },
    "mountains": {
        "label": "Mountains",
        "description": "Rich in minerals, difficult to farm.",
        "multipliers": {
            "agriculture": 0.5,
            "industry": 1.5,
            "energy": 1.2,
            "commerce": 0.7,
            "military": 1.3,
            "research": 0.9,
        },
    },
    "forest": {
        "label": "Forest",
        "description": "Dense woodland with abundant natural resources.",
        "multipliers": {
            "agriculture": 0.9,
            "industry": 1.2,
            "energy": 0.8,
            "commerce": 0.8,
            "military": 1.1,
            "research": 1.0,
        },
    },
    "coast": {
        "label": "Coast",
        "description": "Coastal region with access to sea trade routes.",
        "multipliers": {
            "agriculture": 1.0,
            "industry": 0.9,
            "energy": 1.0,
            "commerce": 1.5,
            "military": 1.0,
            "research": 1.0,
        },
    },
    "desert": {
        "label": "Desert",
        "description": "Harsh arid land with hidden mineral wealth.",
        "multipliers": {
            "agriculture": 0.3,
            "industry": 1.0,
            "energy": 1.4,
            "commerce": 0.6,
            "military": 0.8,
            "research": 0.9,
        },
    },
    "urban_ruins": {
        "label": "Urban Ruins",
        "description": "Pre-war city ruins, rich in salvageable materials and knowledge.",
        "multipliers": {
            "agriculture": 0.4,
            "industry": 1.4,
            "energy": 1.1,
            "commerce": 1.3,
            "military": 0.9,
            "research": 1.5,
        },
    },
    "wasteland": {
        "label": "Wasteland",
        "description": "Irradiated or blighted land. Harsh but unclaimed.",
        "multipliers": {
            "agriculture": 0.2,
            "industry": 0.7,
            "energy": 1.3,
            "commerce": 0.3,
            "military": 0.7,
            "research": 1.1,
        },
    },
    "river_valley": {
        "label": "River Valley",
        "description": "Fertile river basin supporting agriculture and trade.",
        "multipliers": {
            "agriculture": 1.4,
            "industry": 1.0,
            "energy": 1.2,
            "commerce": 1.2,
            "military": 0.9,
            "research": 1.0,
        },
    },
}

# Sector to resource mapping
SECTOR_RESOURCE_MAP = {
    "agriculture": "food",
    "industry": "materials",
    "energy": "energy",
    "commerce": "wealth",
    "military": "manpower",
    "research": "research",
}

# Default sector allocation for new provinces
DEFAULT_SECTOR_ALLOCATION = {
    "agriculture": 40,
    "industry": 20,
    "energy": 15,
    "commerce": 15,
    "military": 5,
    "research": 5,
}

# Base production rate per population unit per sector
BASE_PRODUCTION_RATE = 0.1

# Terrain-specific base populations for new provinces.
# Plains (most fertile arable land) anchors at 10 000.
# Values represent the midpoint; actual starting populations are randomised
# ±30 % around these baselines (rounded to nearest 100).
TERRAIN_BASE_POPULATION = {
    "river_valley": 12000,   # most fertile; strong agriculture + trade
    "plains":       10000,   # baseline
    "coast":         9000,   # good commerce, moderate farming
    "urban_ruins":   8000,   # former city; survivors in the ruins
    "forest":        7000,   # natural resources, harder to settle
    "mountains":     6000,   # mineral-rich but harsh
    "desert":        4000,   # arid; sparse settlement
    "wasteland":     3000,   # harshest; minimal habitation
}

# Fallback when terrain_type is not in TERRAIN_BASE_POPULATION
DEFAULT_PROVINCE_POPULATION = 10000

# --- Province designation system -------------------------------------------
#
# Designation (rural / urban / post_urban) is computed each turn from:
#   score = population + active_completed_buildings × URBAN_BUILDING_WEIGHT
#
# Most provinces stay rural over a 30-year game.  At maximum growth (10%/turn)
# a province starting at 1 000 reaches ~17 400 after 30 turns, so reaching
# URBAN_THRESHOLD (20 000) also requires 1–3 active buildings.
#
# urban_ruins provinces were already cities; their threshold is halved and
# their sub-threshold designation is "post_urban" (not plain "rural").

URBAN_BUILDING_WEIGHT = 15000    # each active, completed building adds this to the score
URBAN_THRESHOLD = 100000         # score needed to become urban (non-ruins terrains)
URBAN_RUINS_URBAN_THRESHOLD = 40000  # lower bar for urban_ruins (former city infrastructure)

# Multipliers applied to subsistence output per resource key.
DESIGNATION_SUBSISTENCE_MODIFIERS = {
    "rural": {
        "food": 1.20, "materials": 1.20, "energy": 1.20,
        "manpower": 1.10, "wealth": 0.90, "research": 0.90,
    },
    "urban": {
        "food": 0.85, "materials": 0.90, "energy": 0.90,
        "manpower": 0.90, "wealth": 1.20, "research": 1.20,
    },
    "post_urban": {
        "food": 0.95, "materials": 1.00, "energy": 1.00,
        "manpower": 1.00, "wealth": 1.10, "research": 1.15,
    },
    # Capital behaves like a moderate urban centre.
    # Government-building bonuses and bureaucratic capacity are not yet
    # implemented; the designation is a placeholder for that future system.
    "capital": {
        "food": 0.90, "materials": 0.90, "energy": 0.90,
        "manpower": 0.90, "wealth": 1.15, "research": 1.15,
    },
}

# Flat multiplier applied to all building output goods.
DESIGNATION_BUILDING_MODIFIER = {
    "rural":      0.90,
    "urban":      1.20,
    "post_urban": 1.10,
    # Slightly above post_urban; will be enhanced once government buildings exist.
    "capital":    1.15,
}
