"""
Provincial Integration System constants.

When a province joins a nation (through economic acquisition, espionage, or
future military/conquest), it starts with its own ideology traits. Over a
normalization period it gradually aligns to the national ideology, after which
it behaves identically to core provinces.

Normalization duration is expressed in turns (1 turn = 1 month).
Base: 10 years = 120 turns.
"""

# ---------------------------------------------------------------------------
# Normalization duration
# ---------------------------------------------------------------------------

# Base normalization period in turns (10 years).
BASE_NORMALIZATION_TURNS = 120

# Trait modifiers to normalization duration.
# Internationalist reduces time (faster integration), Nationalist increases it.
# Strong/weak variant adjustments in turns.
NORMALIZATION_TRAIT_MODIFIERS = {
    "internationalist": {"strong": -48, "weak": -24},  # 6 or 8 years
    "nationalist":      {"strong": +48, "weak": +24},  # 14 or 12 years
}

# ---------------------------------------------------------------------------
# Stability and happiness penalties for non-normalized provinces
# ---------------------------------------------------------------------------

# Maximum stability recovery reduction for a fully mismatched, fresh province.
# Applied as a flat penalty to the stability delta each turn.
# Decreases linearly to 0 as normalization completes.
MAX_NORMALIZATION_STABILITY_PENALTY = 15.0  # points per turn

# Maximum happiness penalty applied after compute_province_happiness().
# Decreases linearly to 0 as normalization completes.
MAX_NORMALIZATION_HAPPINESS_PENALTY = 15.0  # points

# ---------------------------------------------------------------------------
# Ideology mismatch weights
# ---------------------------------------------------------------------------

# Mismatch contribution per differing trait slot.
# 3 slots (1 strong + 2 weak) → each contributes 1/3 at full mismatch.
# Fully opposed (all 3 slots differ): mismatch = 1.0
# 2 slots differ: ~0.67, 1 slot differs: ~0.33, aligned: 0.0
MISMATCH_STRONG_WEIGHT = 1.0 / 3.0
MISMATCH_WEAK_WEIGHT   = 1.0 / 6.0  # each weak slot is half a strong slot

# ---------------------------------------------------------------------------
# Acquisition costs
# ---------------------------------------------------------------------------

# Resource cost to economically acquire an unclaimed province.
# Paid immediately from NationResourcePool.
ECONOMIC_ACQUISITION_COSTS = {
    "wealth":    2000,
    "materials": 1000,
}

# ---------------------------------------------------------------------------
# Espionage persuade_to_join action
# ---------------------------------------------------------------------------

# Number of turns the persuade_to_join espionage action takes to complete.
PERSUADE_ACTION_DURATION = 6  # 6 months

# Minimum Foreign Intelligence Agency policy level required.
PERSUADE_MIN_FIA_LEVEL = 2

# ---------------------------------------------------------------------------
# Unclaimed province ideology drift
# ---------------------------------------------------------------------------

# Probability per turn that an unclaimed province shifts one ideology trait
# toward a random valid value. Base rate corresponds to one full drift per
# normalization period.
UNCLAIMED_DRIFT_RATE = 1.0 / BASE_NORMALIZATION_TURNS
