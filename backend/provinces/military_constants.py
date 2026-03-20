"""
Military system constants.

Unit training, base synergy, and military organisation.
One turn = one month. All rates and costs are monthly.
"""

# Per other-base level in province → training speed bonus (caps at 50%).
MILITARY_BASE_SYNERGY_BONUS = 0.05

BASE_BUILDING_KEYS = ["army_base", "naval_base", "air_base"]

# Map base building key → domain string
UNIT_DOMAINS = {
    "army_base": "army",
    "naval_base": "navy",
    "air_base": "air",
}

# Map domain string → base building key
DOMAIN_TO_BASE = {
    "army": "army_base",
    "navy": "naval_base",
    "air": "air_base",
}

# Unit types each domain can train
DOMAIN_UNITS = {
    "army": ["militia", "infantry", "motorized", "armored", "artillery"],
    "navy": ["patrol_boat", "frigate", "transport"],
    "air": ["scout_plane", "fighter", "bomber"],
}

UNIT_TYPES = {
    # -------------------------------------------------------
    # ARMY — trained by Army Base
    # -------------------------------------------------------
    "militia": {
        "domain": "army",
        "name": "Militia",
        "description": "Lightly armed local defenders.",
        "military_goods_cost": 50,
        "manpower_cost": 100,
        "construction_turns": 3,
        "upkeep": {"military_goods": 5},
    },
    "infantry": {
        "domain": "army",
        "name": "Infantry",
        "description": "Standard trained foot soldiers.",
        "military_goods_cost": 150,
        "manpower_cost": 200,
        "construction_turns": 6,
        "upkeep": {"military_goods": 15, "food": 10},
    },
    "motorized": {
        "domain": "army",
        "name": "Motorized Infantry",
        "description": "Vehicle-mobile infantry able to move and engage rapidly.",
        "military_goods_cost": 300,
        "manpower_cost": 300,
        "construction_turns": 9,
        "upkeep": {"military_goods": 30, "fuel": 20},
    },
    "armored": {
        "domain": "army",
        "name": "Armored Unit",
        "description": "Tank and armored vehicle formations providing breakthrough capability.",
        "military_goods_cost": 600,
        "manpower_cost": 200,
        "construction_turns": 12,
        "upkeep": {"military_goods": 60, "fuel": 40},
    },
    "artillery": {
        "domain": "army",
        "name": "Artillery",
        "description": "Long-range fire support units.",
        "military_goods_cost": 500,
        "manpower_cost": 250,
        "construction_turns": 10,
        "upkeep": {"military_goods": 50, "fuel": 30},
    },

    # -------------------------------------------------------
    # NAVY — trained by Naval Base (coastal or river only)
    # -------------------------------------------------------
    "patrol_boat": {
        "domain": "navy",
        "name": "Patrol Boat",
        "description": "Fast coastal patrol and interdiction vessel.",
        "military_goods_cost": 200,
        "manpower_cost": 100,
        "construction_turns": 6,
        "upkeep": {"military_goods": 20, "fuel": 15},
    },
    "frigate": {
        "domain": "navy",
        "name": "Frigate",
        "description": "Multi-role warship capable of fleet and convoy operations.",
        "military_goods_cost": 600,
        "manpower_cost": 300,
        "construction_turns": 15,
        "upkeep": {"military_goods": 60, "fuel": 40},
    },
    "transport": {
        "domain": "navy",
        "name": "Transport",
        "description": "Logistical vessel for moving troops and supplies across water.",
        "military_goods_cost": 400,
        "manpower_cost": 200,
        "construction_turns": 10,
        "upkeep": {"military_goods": 30, "fuel": 25},
    },

    # -------------------------------------------------------
    # AIR — trained by Air Base
    # -------------------------------------------------------
    "scout_plane": {
        "domain": "air",
        "name": "Scout Plane",
        "description": "Reconnaissance aircraft providing intelligence on enemy positions.",
        "military_goods_cost": 300,
        "manpower_cost": 100,
        "construction_turns": 8,
        "upkeep": {"military_goods": 30, "fuel": 50},
    },
    "fighter": {
        "domain": "air",
        "name": "Fighter",
        "description": "Air superiority aircraft engaging enemy planes and ground targets.",
        "military_goods_cost": 500,
        "manpower_cost": 150,
        "construction_turns": 12,
        "upkeep": {"military_goods": 50, "fuel": 70},
    },
    "bomber": {
        "domain": "air",
        "name": "Bomber",
        "description": "Strategic bombing aircraft capable of deep strikes against infrastructure.",
        "military_goods_cost": 800,
        "manpower_cost": 200,
        "construction_turns": 16,
        "upkeep": {"military_goods": 80, "fuel": 100},
    },
}
