"""
Research unlock system constants.

Research accumulates in NationResourcePool.research each turn. Spending research
unlocks higher building levels for an entire sector (building category).

Building level gating:
  Base max level (no unlock) = 2  (L1 and L2 always available)
  Tier 1 unlock: opens L3-L4
  Tier 2 unlock: opens L5-L6  (future use when buildings go above L3)

Unlocks are sequential: Tier 2 requires Tier 1 to already be purchased.

National literacy multiplies research production each turn:
  research_output *= (RESEARCH_LITERACY_BASE + national_literacy * RESEARCH_LITERACY_SCALE)
  At 20% literacy: 0.5× multiplier (early game research is slow)
  At 80% literacy: 1.1× multiplier
  At 100% literacy: 1.3× multiplier (bonus for high-literacy nations)

Research production estimate:
  Early game: ~100 raw research/turn from 1 Research Institute (L1) + subsistence
  At 20% literacy: ~50 effective research/turn
  First Tier-1 unlock achievable around turn 60–90 (years 5–8).
"""

# Base building level available without any research unlock.
BASE_MAX_BUILDING_LEVEL = 2

# ---------------------------------------------------------------------------
# Literacy ↔ research multiplier
# ---------------------------------------------------------------------------

# national_research *= (RESEARCH_LITERACY_BASE + national_literacy * RESEARCH_LITERACY_SCALE)
RESEARCH_LITERACY_BASE = 0.3
RESEARCH_LITERACY_SCALE = 1.0

# ---------------------------------------------------------------------------
# Military research cost modifiers from ideology traits
# (applied when implementing military unit research — stub values stored here)
# ---------------------------------------------------------------------------

MILITARY_RESEARCH_TRAIT_MULTS = {
    "militarist": {"strong": 0.75, "weak": 0.90},   # -25% / -10% cost
    "pacifist":   {"strong": 1.50, "weak": 1.25},   # +50% / +25% cost
}

# ---------------------------------------------------------------------------
# Trait multipliers on literacy_bonus and research from specific building categories
# Stored as: {trait: {strength: {category: multiplier}}}
# Applied during building production for research-producing buildings.
# ---------------------------------------------------------------------------

TRAIT_BUILDING_LIT_RESEARCH_MULTS = {
    "spiritualist": {
        "strong": {"religious": 1.30},
        "weak":   {"religious": 1.10},
    },
    "modern": {
        "strong": {"government_education": 1.30},
        "weak":   {"government_education": 1.10},
    },
    "industrialist": {
        "strong": {"heavy_manufacturing": 1.30, "refining": 1.30},
        "weak":   {"heavy_manufacturing": 1.10, "refining": 1.10},
    },
}

# ---------------------------------------------------------------------------
# Research unlock costs per sector, per tier
# Format: {sector_key: {tier: cost}}
# Tier 2 costs = 4× Tier 1 costs (future-proofed for L5-L6 buildings)
# ---------------------------------------------------------------------------

_TIER1 = {
    "heavy_manufacturing":  5000,
    "light_manufacturing":  4000,
    "refining":             5000,
    "chemical":             5500,
    "pharmaceutical":       6000,
    "farming":              3000,
    "extraction":           3500,
    "construction":         4000,
    "financial":            4500,
    "transport":            4000,
    "communications":       5000,
    "entertainment":        3500,
    "healthcare":           5000,
    "religious":            3000,
    "green_energy":         5500,
    "government_regulatory":  4000,
    "government_oversight":   4000,
    "government_management":  4000,
    "government_security":    4000,
    "government_education":   4000,
    "government_organization": 4000,
    "government_welfare":     4000,
    "military_education":     6000,
    "espionage_attack":       5500,
    "espionage_defense":      5000,
    "military_army":          5000,
    "military_naval":         5500,
    "military_air":           6000,
}

RESEARCH_UNLOCK_COSTS = {sector: {1: cost, 2: cost * 4} for sector, cost in _TIER1.items()}
