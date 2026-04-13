"""
Bureaucratic Capacity System — constants and static data.

All static configuration for the bureaucratic capacity system:
  - Base cost and ramp formula
  - Tier consumption rules (how many tiers consume capacity by policy size)
  - Policy category classification (business / neutral / individual)
  - Government axis multipliers on total capacity
  - Trait multipliers on total capacity
  - Exempt policy categories
  - Deficit penalty rates
  - Treaty stub cost
"""

# ---------------------------------------------------------------------------
# Cost formula constants
# ---------------------------------------------------------------------------

# Cost of the lowest consuming tier for any policy
BUREAUCRATIC_BASE_COST = 5

# Multiplier applied to each successive consuming tier (exponential ramp)
# lowest consuming = BUREAUCRATIC_BASE_COST
# next = BUREAUCRATIC_BASE_COST × BUREAUCRATIC_COST_MULTIPLIER
# top  = BUREAUCRATIC_BASE_COST × BUREAUCRATIC_COST_MULTIPLIER^(n-1)
BUREAUCRATIC_COST_MULTIPLIER = 2

# Stub cost for entering/enforcing a treaty (future diplomacy system)
TREATY_BUREAUCRATIC_BASE_COST = 10

# ---------------------------------------------------------------------------
# Tier consumption rules
# Indexed by number of tiers in a policy category.
# Values: number of top tiers that consume bureaucratic capacity.
# ---------------------------------------------------------------------------

def get_consuming_tier_count(total_tiers: int) -> int:
    """Return how many top tiers consume capacity for a policy of this size."""
    if total_tiers <= 3:
        return 1
    elif total_tiers <= 5:
        return 2
    elif total_tiers <= 7:
        return 3
    else:
        return 4


# ---------------------------------------------------------------------------
# Policy category classification
# ---------------------------------------------------------------------------

# All 63 policy categories classified into three buckets.
# business  : primarily regulates/supports business activity (0.8× cost)
# neutral   : state apparatus, governance, military (1.0× cost)
# individual: regulates individual rights and welfare (1.2× cost)

BUREAUCRATIC_CATEGORY_TYPE = {
    # --- Business (0.8×) ---
    "industrial_subsidies":     "business",
    "resource_subsidies":       "business",
    "agricultural_subsidies":   "business",
    "firms":                    "business",
    "market":                   "business",
    "firm_size":                "business",
    "currency":                 "business",
    "property_rights":          "business",
    "land_ownership":           "business",
    "consumer_protections":     "business",
    "unions":                   "business",
    "minimum_wage":             "business",
    "working_hours":            "business",

    # --- Neutral / Government (1.0×) ---
    "military_service":              "neutral",
    "policing":                      "neutral",
    "domestic_intelligence_agency":  "neutral",
    "foreign_intelligence_agency":   "neutral",
    "martial_law":                   "neutral",
    "bureaucracy":                   "neutral",
    "legal_system":                  "neutral",
    "punishments":                   "neutral",
    "income_tax":                    "neutral",
    "consumption_tax":               "neutral",
    "land_tax":                      "neutral",
    "gift_and_estate_taxes":         "neutral",
    "prison_system":                 "neutral",
    "educational_philosophy":        "neutral",
    "conservation":                  "neutral",
    "government_salary":             "neutral",
    "government_benefits":           "neutral",
    "health_and_safety_regulations": "neutral",
    "military_recruitment_standards":"neutral",
    "military_salaries":             "neutral",
    "anti_corruption_policy":        "neutral",
    "mobilization":                  "neutral",

    # --- Individual (1.2×) ---
    "freedom_of_movement":      "individual",
    "freedom_of_association":   "individual",
    "freedom_of_press":         "individual",
    "freedom_of_speech":        "individual",
    "suffrage":                 "individual",
    "gender_rights":            "individual",
    "racial_rights":            "individual",
    "gender_roles":             "individual",
    "social_discrimination":    "individual",
    "sexuality":                "individual",
    "education":                "individual",
    "pensions":                 "individual",
    "healthcare":               "individual",
    "immigration":              "individual",
    "vice":                     "individual",
    "civilian_firearm_ownership": "individual",
    "drug_policy":              "individual",
    "family_planning":          "individual",
    "child_labor":              "individual",
    "slavery":                  "individual",
    "slavery_type":             "individual",
    "maternity_leave":          "individual",
    "paternity_leave":          "individual",
    "holidays":                 "individual",
    "birthright_citizenship":   "individual",
    "naturalization_laws":      "individual",
    "visa_policy":              "individual",
    "emmigration_policy":       "individual",
}

CATEGORY_COST_MULTIPLIERS = {
    "business":   0.8,
    "neutral":    1.0,
    "individual": 1.2,
}

# ---------------------------------------------------------------------------
# Exempt policy categories (zero bureaucratic cost regardless of tier)
# ---------------------------------------------------------------------------

# Feminist, anti-slavery, and racial-equity policies are always free.
ALWAYS_EXEMPT_CATEGORIES = frozenset({
    "gender_rights",       # feminist
    "gender_roles",        # feminist
    "slavery",             # anti-slavery
    "slavery_type",        # anti-slavery
    "racial_rights",       # racial equity
    "social_discrimination",  # racial equity
})

# Ecologist trait exempts these categories at consuming tiers only.
ECOLOGIST_EXEMPT_CATEGORIES = frozenset({
    "conservation",
    "health_and_safety_regulations",
    "drug_policy",
})

# ---------------------------------------------------------------------------
# Government axis multipliers on total bureaucratic capacity
# ---------------------------------------------------------------------------
#
# Each government axis value has an independent multiplier. The five axis
# multipliers are multiplied together, then clamped to [0.50, 2.00].
#
# Values not listed here default to 1.00.

GOV_BUREAUCRATIC_CAPACITY_MULTIPLIER = {
    # GOV_DIRECTION
    "top_down":   1.20,   # big bonus: centralized command = efficient bureaucracy
    "bottom_up":  1.00,
    "none":       0.95,   # slight friction without a clear governing direction

    # GOV_ECONOMIC_CATEGORY
    "liberal":       1.00,
    "collectivist":  1.10,   # small bonus: organized economy supports admin
    "protectionist": 1.00,
    "resource":      0.90,   # small malus: extraction focus, not administration
    "autarkic":      1.00,
    "subsistence":   0.95,

    # GOV_STRUCTURE
    "hereditary":     1.00,
    "power_consensus":1.00,
    "federal":        0.95,
    "representative": 1.10,  # small bonus: institutional capacity
    "direct":         1.00,

    # GOV_POWER_ORIGIN
    "elections":        1.10,  # small bonus: legitimacy aids bureaucratic compliance
    "economic_success": 1.00,
    "law_and_order":    1.05,
    "military_power":   0.90,  # small malus: military logic crowds out civilian admin
    "religious":        0.95,
    "ideology":         1.00,

    # GOV_POWER_TYPE
    "singular":        1.20,  # big bonus: unified decision-making
    "council":         1.05,
    "large_body":      1.00,
    "multi_body":      0.90,  # small malus: coordination overhead across bodies
    "staggered_groups":0.80,  # big malus: staggered terms create administrative gridlock
}

# Combined government multiplier is clamped to this range.
GOV_MULTIPLIER_MIN = 0.50
GOV_MULTIPLIER_MAX = 2.00

# ---------------------------------------------------------------------------
# Trait multipliers on total bureaucratic capacity
# ---------------------------------------------------------------------------
#
# Format: trait_key -> {"strong": multiplier, "weak": multiplier}

TRAIT_BUREAUCRATIC_CAPACITY_MULTIPLIER = {
    "modern":      {"strong": 1.15, "weak": 1.08},
    "libertarian": {"strong": 0.85, "weak": 0.92},
}

# Internationalist treaty cost reduction (stub — diplomacy system not yet built).
# Format: trait_key -> {"strong": fraction_reduction, "weak": fraction_reduction}
TRAIT_TREATY_COST_REDUCTION = {
    "internationalist": {"strong": 0.30, "weak": 0.15},
}

# ---------------------------------------------------------------------------
# Deficit penalty constants
# ---------------------------------------------------------------------------

# Per 1% of deficit ratio, apply this many stability points of penalty per turn.
# E.g. 20% deficit → 20 × 0.5 = 10 stability penalty (capped below).
DEFICIT_STABILITY_PENALTY_PER_PCT = 0.5

# Maximum monthly stability penalty from bureaucratic deficit.
DEFICIT_STABILITY_PENALTY_CAP = 10.0
