"""
Travel time constants and speed parameters. All times in turns (1 turn = 1 month).

Travel time formulas:
  Province->Province:  distance(center_a, center_b) / (MARCH_SPEED * (1 + march_speed_bonus))
  Province->Sea/River: border_distance / (EMBARK_SPEED * (1 + transit_speed_bonus))
  Zone->Zone (same):   BASE_ZONE_TRAVEL[zone_type] / (1 + zone_speed_bonus)
  Free transitions:    listed in FREE_CROSS_TYPE_TRANSITIONS

Coordinates are in abstract map units (set by GM when map is developed).
MARCH_SPEED and EMBARK_SPEED are in map units per turn.

Province coordinates and border distances are nullable. When null, the
fallback constants DEFAULT_MARCH_TIME and DEFAULT_EMBARK_TIME are used.
"""

# Speed in map units per turn (calibrate to map scale when map is ready)
MARCH_SPEED  = 100.0   # province-to-province march speed
EMBARK_SPEED = 1000.0  # embarkation/crossing speed (10x march -> "far less than 1 turn")

# Fallback flat times used when province coordinates/border distances are null
DEFAULT_MARCH_TIME  = 1.0     # 1 turn per province hop if no coordinates set
DEFAULT_EMBARK_TIME = 0.1     # 0.1 turns cross-type if no border distance set

# Base turns for zone-to-zone same-type travel (no coordinates yet for zones)
BASE_ZONE_TRAVEL = {
    'sea':   1.0,
    'river': 1.0,
    'air':   1.0,
}

# Cross-type transitions that cost zero turns (no embarkation overhead)
FREE_CROSS_TYPE_TRANSITIONS = {
    ('sea',   'air'),
    ('air',   'sea'),
    ('river', 'air'),
    ('air',   'river'),
}

# Cross-type transitions that require specific buildings at the province end.
# Values are list[list[str]] where each inner list is an "any of" group.
CROSS_TYPE_REQUIREMENTS = {
    ('province', 'sea'):   [['dock']],                  # dock required at province
    ('sea',   'province'): [['dock']],                  # dock required at destination province
    ('province', 'air'):   [['air_base', 'airport']],   # either satisfies requirement
    ('air',   'province'): [['air_base', 'airport']],
    ('province', 'river'): [],
    ('river', 'province'): [],
    ('sea',   'river'):    [],
    ('river', 'sea'):      [],
}

# Building effect key that modifies each zone type's same-type travel
ZONE_SPEED_MODIFIER_KEY = {
    'sea':   'sea_transit_speed',
    'river': 'river_transit_speed',
    'air':   'air_transit_speed',
}

# Province-scope effect keys used for cross-type transitions FROM a province
CROSS_TYPE_PROVINCE_MODIFIER_KEY = {
    'sea':   'sea_transit_speed',
    'river': 'river_transit_speed',
    'air':   'air_transit_speed',
}

MINIMUM_TRAVEL_TURNS = 0.01  # absolute floor — a dock+airbase can't teleport units
