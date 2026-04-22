"""
Development Points (DP) System — constants (System 17).

DP is a per-province, per-building-category score that provides a
multiplicative bonus on final building output (multiplier of multipliers).
"""

# ---------------------------------------------------------------------------
# DP Categories
# ---------------------------------------------------------------------------

# All non-military building categories (one DP row per province per category).
DP_BUILDING_CATEGORIES = [
    # agriculture sector
    "farming",
    # extraction sector
    "extraction",
    # industry sector
    "heavy_manufacturing",
    "light_manufacturing",
    "chemical",
    "construction",
    # energy sector
    "green_energy",
    "refining",
    # commerce sector
    "financial",
    "transport",
    "communications",
    # research sector
    "pharmaceutical",
    "healthcare",
    # unmapped (no sector in SECTOR_BUILDING_CATEGORY_MAP)
    "entertainment",
    "religious",
    "government_regulatory",
    "government_oversight",
    "government_management",
    "government_security",
    "government_education",
    "government_organization",
    "government_welfare",
    "espionage_attack",
    "espionage_defense",
]

# Full category list including subsistence.
DP_ALL_CATEGORIES = DP_BUILDING_CATEGORIES + ["subsistence"]

# Military DP — stub only (constants defined, no models or mechanics).
MILITARY_DP_CATEGORIES = ["strategy", "tactics", "logistics"]

# ---------------------------------------------------------------------------
# Sector → building category mapping (for terrain-weighted init).
# Reverse lookup from SECTOR_BUILDING_CATEGORY_MAP.
# Unmapped building categories map to None.
# ---------------------------------------------------------------------------
BUILDING_CATEGORY_TO_SECTOR = {
    "farming":              "agriculture",
    "extraction":           "extraction",
    "heavy_manufacturing":  "industry",
    "light_manufacturing":  "industry",
    "chemical":             "industry",
    "construction":         "industry",
    "green_energy":         "energy",
    "refining":             "energy",
    "financial":            "commerce",
    "transport":            "commerce",
    "communications":       "commerce",
    "pharmaceutical":       "research",
    "healthcare":           "research",
    # Unmapped — no terrain multiplier, default weight 1.0
    "entertainment":        None,
    "religious":            None,
    "government_regulatory": None,
    "government_oversight": None,
    "government_management": None,
    "government_security":  None,
    "government_education": None,
    "government_organization": None,
    "government_welfare":   None,
    "espionage_attack":     None,
    "espionage_defense":    None,
}

# ---------------------------------------------------------------------------
# Multiplier curve
# ---------------------------------------------------------------------------
# Formula: 1 + dp / (dp + K)
# dp=0   → 1.0 (no bonus)
# dp=K   → 1.5 (midpoint)
# dp=∞   → 2.0 (limit)
DP_MULTIPLIER_K = 100

# ---------------------------------------------------------------------------
# Concentration bonus/penalty
# ---------------------------------------------------------------------------
# Triggers when one category holds >50% of a province's total DP.
#   Concentrated category:  1 + ((cat_dp - total_dp/2) / BONUS_DIVISOR)
#   All other categories:   1 - ((cat_dp - total_dp/2) / PENALTY_DIVISOR)
# Penalty is clamped to a floor of 0.0.
CONCENTRATION_BONUS_DIVISOR = 50
CONCENTRATION_PENALTY_DIVISOR = 10

# ---------------------------------------------------------------------------
# DP transfer (inter-category, per-turn order)
# ---------------------------------------------------------------------------
# Spend COST_RATIO DP from source to gain 1 in target.
DP_TRANSFER_COST_RATIO = 2

# ---------------------------------------------------------------------------
# Annual DP grant
# ---------------------------------------------------------------------------
DP_ANNUAL_GRANT = 40        # DP granted per nation every grant interval
DP_GRANT_INTERVAL = 12      # turns between grants (1 year)

# ---------------------------------------------------------------------------
# Military DP conversion
# ---------------------------------------------------------------------------
DP_MILITARY_COST_RATIO = 4  # spend 4 provincial DP to gain 1 military DP

# ---------------------------------------------------------------------------
# Expansion slot purchase
# ---------------------------------------------------------------------------
DP_EXPANSION_COST = 5       # DP cost per expansion slot

# ---------------------------------------------------------------------------
# Game-start initialization
# ---------------------------------------------------------------------------
DP_INIT_TOTAL_MIN = 100     # min starting non-subsistence DP per province
DP_INIT_TOTAL_MAX = 200     # max starting non-subsistence DP per province
DP_INIT_SUBSISTENCE_MIN = 20
DP_INIT_SUBSISTENCE_MAX = 40
