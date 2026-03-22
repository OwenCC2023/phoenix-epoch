# Government types are now defined by five orthogonal components in
# nations/government_constants.py.  See GOV_DIRECTION, GOV_ECONOMIC_CATEGORY,
# GOV_STRUCTURE, GOV_POWER_ORIGIN, and GOV_POWER_TYPE there, plus the
# get_combined_government_effects() helper.

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
