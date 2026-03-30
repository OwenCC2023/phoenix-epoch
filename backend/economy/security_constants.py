BASE_SECURITY = 30.0

# Stability multiplier curve: linear 0-50, logarithmic 50-100
# At security  0 → 0.50
# At security 30 → 0.90  (base)
# At security 50 → 1.167
# At security 75 → 1.362
# At security 100→ 1.50
SECURITY_STABILITY_FLOOR = 0.5
SECURITY_STABILITY_CAP = 1.5

# Literacy multiplier curve: linear 0-50, logarithmic 50-100
# At security  0 → 0.70
# At security 30 → 0.90  (base)
# At security 50 → 1.033
# At security 100→ 1.20
SECURITY_LITERACY_FLOOR = 0.7
SECURITY_LITERACY_CAP = 1.2

# Growth bonus: small positive above security 50
SECURITY_GROWTH_THRESHOLD = 50
SECURITY_GROWTH_MAX_BONUS = 0.005  # +0.5%/month at security 100

# Food deficit flat penalties applied after multiplicative modifiers
SECURITY_FOOD_DEFICIT_PENALTY = -8.0    # food ratio 0.5–1.0
SECURITY_FOOD_SEVERE_PENALTY = -15.0   # food ratio < 0.5

# Immigration penalty (per 1% of province population that immigrated this turn)
SECURITY_IMMIGRATION_PENALTY_RATE = -0.5   # per 1% net immigration
SECURITY_IMMIGRATION_PENALTY_CAP = -10.0  # maximum penalty from immigration
