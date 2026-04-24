"""Constants for the Wealth & Taxation pricing / market system.

See docs/systems/wealth_taxation_system.md for the full pricing model.
"""

# --- Shortage factor bounds -----------------------------------------------

SHORTAGE_FACTOR_MIN = 0.5
SHORTAGE_FACTOR_MAX = 3.0

# --- Base land values (food-equivalent, per-province Land Tax base) -------

BASE_LAND_VALUE = {
    "river_valley": 500,
    "plains":       400,
    "coast":        350,
    "urban_ruins":  300,
    "forest":       250,
    "mountains":    200,
    "desert":       150,
    "wasteland":    100,
}

# --- Good classifications (for structure multipliers in tax policies) -----

BASIC_RESOURCES = ("food", "materials", "energy", "kapital")
BASIC_RESOURCES_SET = frozenset(BASIC_RESOURCES)

# Goods outside the market pricing system — produced but not priced or traded.
SPECIAL_GOODS = frozenset({"manpower", "research"})

# Good-class groupings for Consumption Tax structure multipliers.
SIN_GOODS      = frozenset({"arms", "fuel", "entertainment"})
HARMFUL_GOODS  = frozenset({"fuel", "chemicals", "arms"})
MEDICINE_GOODS = frozenset({"medicine"})

# --- Debt interest ---------------------------------------------------------

DEBT_INTEREST_BASE = 0.02       # 2% base monthly rate when in debt
DEBT_INTEREST_SCALE = 500       # interest doubles at 500 food-equiv debt

# --- Subsidy sector → goods --------------------------------------------------

# A subsidy on a sector purchases from the national market in that sector's
# output goods, injecting demand and raising shortage_factor → price.
# Keys match building-category sectors (see SECTOR_BUILDING_CATEGORY_MAP).
SUBSIDY_SECTOR_MAP = {
    "agriculture": ["food"],
    "extraction":  ["materials"],
    "industry":    ["machinery", "components", "heavy_equipment", "consumer_goods", "chemicals", "arms"],
    "energy":      ["energy", "fuel"],
    "commerce":    ["kapital", "consumer_goods"],
    "research":    ["medicine"],
}
