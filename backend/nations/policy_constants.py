"""
Policy category definitions.

63 categories sourced from policy_effects_complete.xlsx "Corrected Policy Effects" sheet.
Each category has 2-8 discrete levels with simulation effects.

Category/level data and base effects are in policy_effects_data.py (auto-generated).
This file re-exports those and adds validation/interaction dicts.

Interaction data (disabling rules, building forbidden) is in:
  - disabling_rules.py — trait/gov/policy disabling cascade
  - policy_building_forbidden.py — policy→building forbidden rules
These are wired into policy_effects.py in Phase 3.
"""

from .policy_effects_data import POLICY_CATEGORIES, POLICY_EFFECTS

# Convenience: total number of policy categories
POLICY_CATEGORY_COUNT = len(POLICY_CATEGORIES)


# =============================================================================
# POLICY_REQUIREMENTS — prerequisites to select a policy level
#
# Keys: (category, level_index) -> dict with optional keys:
#   "gov_axis_required": nation must have at least one of these axis values
#   "gov_axis_banned":   nation must not have any of these axis values
#   "traits_required":   list of trait keys (must have at least one)
#   "traits_banned":     list of trait keys (must not have any)
#   "policies_required": list of (category, min_level) tuples
#
# Populated from disabling_rules.py in Phase 3.
# =============================================================================

POLICY_REQUIREMENTS = {}


# =============================================================================
# POLICY_BANS — cross-policy incompatibilities
#
# When a nation has (category, level), the listed (category, level) combos
# become unavailable.  Checked symmetrically: both sides are listed.
#
# Populated from disabling_rules.py POLICY_POLICY_DISABLES in Phase 3.
# =============================================================================

POLICY_BANS = {}


# =============================================================================
# BUILDING_POLICY_REQUIREMENTS — buildings that need specific policy levels
#
# Format: building_type -> list of (policy_category, min_level_index) tuples.
# ALL requirements must be met (AND logic).
# =============================================================================

BUILDING_POLICY_REQUIREMENTS = {}


# =============================================================================
# BUILDING_POLICY_BANS — buildings blocked by specific policy levels
#
# Format: building_type -> list of (policy_category, exact_level) tuples.
# ANY match blocks construction.
#
# Populated from policy_building_forbidden.py in Phase 3.
# =============================================================================

BUILDING_POLICY_BANS = {}


# =============================================================================
# UNIT_POLICY_REQUIREMENTS — unit types requiring specific policy levels
#
# Format: unit_type -> list of (policy_category, min_level) tuples.
# ALL requirements must be met.
#
# Stub — will be populated when military system is built.
# =============================================================================

UNIT_POLICY_REQUIREMENTS = {
    "militia": [],
    "infantry": [("military_service", 1)],
    "motorized": [("military_service", 2)],
    "armored": [("military_service", 3)],
    "artillery": [("military_service", 2)],
    "patrol_boat": [("military_service", 1)],
    "frigate": [("military_service", 3)],
    "transport": [("military_service", 2)],
    "scout_plane": [("military_service", 2)],
    "fighter": [("military_service", 3)],
    "bomber": [("military_service", 4)],
}


# =============================================================================
# UNIT_POLICY_BANS — unit types blocked by specific policy levels
#
# Format: unit_type -> list of (policy_category, exact_level) tuples.
# ANY match blocks training.
# =============================================================================

UNIT_POLICY_BANS = {
    "militia": [("military_service", 0)],
    "infantry": [("military_service", 0)],
    "motorized": [("military_service", 0)],
    "armored": [("military_service", 0)],
    "artillery": [("military_service", 0)],
    "patrol_boat": [("military_service", 0)],
    "frigate": [("military_service", 0)],
    "transport": [("military_service", 0)],
    "scout_plane": [("military_service", 0)],
    "fighter": [("military_service", 0)],
    "bomber": [("military_service", 0)],
}
