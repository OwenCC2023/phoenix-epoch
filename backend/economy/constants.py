"""Government types, ideologies, and their modifier definitions."""

# Government types provide national-level modifiers.
# Keys in sub-dicts map to modifier categories.
# 'production' is a dict of resource: percentage_bonus
# Other keys are single values (percentage or flat for stability)
# Growth modifier values are per-month rates (turns are months).
# Annualised: multiply by 12 for approximate yearly impact.
# e.g. democracy growth 0.002/month ≈ +2.4 %/year population bonus.
GOVERNMENT_TYPES = {
    "democracy": {
        "production": {"wealth": 0.10},
        "integration": 0.05,
        "stability": 2,
        "growth": 0.002,       # ~+2.4 %/year
        "consumption": 0.05,
        # Open markets and information flow benefit finance and communications.
        "building_efficiency": {"financial": 0.10, "communications": 0.08},
    },
    "autocracy": {
        "production": {"materials": 0.10, "manpower": 0.05},
        "integration": 0.10,
        "stability": -3,
        "growth": -0.001,      # ~−1.2 %/year
        "consumption": -0.05,
        # Command economy excels at directed heavy industry and resource extraction.
        "building_efficiency": {"heavy_manufacturing": 0.10, "extraction": 0.08},
    },
    "theocracy": {
        "production": {"wealth": 0.05},
        "stability": 5,
        "growth": 0.002,       # ~+2.4 %/year
        "trade": -0.10,
        "research": -0.10,
        # Community welfare institutions, grain tithes, and religious authority.
        "building_efficiency": {"farming": 0.08, "healthcare": 0.10, "religious": 0.12},
    },
    "junta": {
        "production": {"manpower": 0.15},
        "integration": 0.08,
        "stability": -5,
        "military": 0.15,
        "consumption": -0.10,
        # State-directed infrastructure projects and arms production.
        "building_efficiency": {"construction": 0.10, "heavy_manufacturing": 0.08},
    },
    "tribal": {
        "production": {"food": 0.10},
        "integration": -0.10,
        "stability": 3,
        "growth": 0.004,       # ~+4.9 %/year — tribal communities are fertile
        "trade": -0.15,
        # Subsistence expertise and deep land knowledge.
        "building_efficiency": {"farming": 0.12, "extraction": 0.08},
    },
    "corporate": {
        "production": {"wealth": 0.15, "energy": 0.05},
        "integration": 0.05,
        "stability": -2,
        "trade": 0.15,
        "growth": -0.002,      # ~−2.4 %/year
        # Profit-maximising logistics and financial sector.
        "building_efficiency": {"financial": 0.12, "transport": 0.08},
    },
    "commune": {
        "production": {"food": 0.05, "materials": 0.05},
        "integration": -0.05,
        "stability": 4,
        "growth": 0.002,       # ~+2.4 %/year
        "trade": -0.05,
        "consumption": -0.10,
        # Collective labour pools for food security and local craft goods.
        "building_efficiency": {"farming": 0.10, "light_manufacturing": 0.08},
    },
}

# Default integration efficiency (percentage of province surplus that reaches national pool)
BASE_INTEGRATION_EFFICIENCY = 0.85

# Food consumption per population unit per turn.
# At 0.06 a plains province (10 000 pop, SUBSISTENCE_RATE 0.05, terrain ×1.5,
# rural ×1.20) produces 900 food vs 600 consumed — a +300 surplus that flows
# to the national pool to feed importing provinces.  Non-food provinces still
# depend entirely on imports; the ratio rewards agricultural specialisation
# without making food trivially abundant.
FOOD_CONSUMPTION_PER_POP = 0.06

# Stability thresholds — per month (turns are months).
# Annualised: deficit costs ~2.4 stability/year; recovery earns ~3.6/year.
# Non-food provinces that are covered by the national stockpile won't trigger
# the deficit penalty, so only genuinely underfed provinces lose stability.
STABILITY_FOOD_DEFICIT_PENALTY = 0.2  # per month of deficit  (~2.4/year)
STABILITY_RECOVERY_RATE        = 0.3  # per month when well-fed (~3.6/year)

# Collapse condition.
# 6 consecutive months of nation-wide food deficit → collapse.
# (Was 3 annual turns; 6 months is the monthly equivalent at roughly the same
# real-time severity — half a year of total starvation is unrecoverable.)
COLLAPSE_STARVATION_TURNS = 6
