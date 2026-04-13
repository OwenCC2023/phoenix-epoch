"""
Control, Regions, and Rebellion System constants.

Control is a per-province value (1–100%) representing how tightly the national
government governs that province. Provinces in a Region inherit the region's
control value. Control gates how much of provincial production flows nationally
and drives rebellion risk.
"""

# ---------------------------------------------------------------------------
# Control Bounds
# ---------------------------------------------------------------------------

CONTROL_MIN = 1.0     # absolute floor — provinces always have some local activity
CONTROL_MAX = 100.0   # full central government control
CONTROL_DEFAULT = 100.0

# ---------------------------------------------------------------------------
# Production Bonus
# ---------------------------------------------------------------------------
# Lower control lets local producers operate with less interference, boosting
# output — but the national government captures less of it.
#
# Formula: production_bonus = PRODUCTION_BONUS_MAX * (1 - control/100)
# At 100% control: +0% bonus. At 1% control: ~+24.75% bonus.
# Applies to materials, energy, and wealth only (not food or manpower).
PRODUCTION_BONUS_MAX = 0.25

# ---------------------------------------------------------------------------
# National Flow Fraction
# ---------------------------------------------------------------------------
# Fraction of province surplus that reaches the national pool.
# Formula: national_flow = control / 100.0
# The retained fraction (1 - flow) is tracked in ControlPoolSnapshot.

# ---------------------------------------------------------------------------
# Normalization Time Scaling
# ---------------------------------------------------------------------------
# For every NORMALIZATION_DOUBLING_THRESHOLD percentage points below 100%,
# the normalization duration doubles.
# At 60% control: 2× time. At 20% control: 4× time.
NORMALIZATION_DOUBLING_THRESHOLD = 40.0

# ---------------------------------------------------------------------------
# Espionage Effects
# ---------------------------------------------------------------------------
# Lower control weakens the national defense presence in the province and
# makes it easier for foreign intelligence to gather information.
#
# Defense multiplier = control / 100 (applied to national_defense average)
# Transparency bonus at minimum control:
ESPIONAGE_TRANSPARENCY_BONUS_MAX = 0.30

# ---------------------------------------------------------------------------
# Ideology-Control Interactions
# ---------------------------------------------------------------------------

# Libertarian: more stability and happiness in low-control provinces.
# Bonus = MAX * (1 - control/100); scaled by strong (1.0) / weak (0.5).
LIBERTARIAN_LOW_CONTROL_STABILITY_BONUS = 5.0   # max per-province stability bonus
LIBERTARIAN_LOW_CONTROL_HAPPINESS_BONUS = 5.0   # max per-province happiness bonus

# Authoritarian: national happiness penalty when any province is below 100%.
# penalty_per_province = UNHAPPY_PER_PCT * (100 - control) / 100
# Summed across all provinces, capped at UNHAPPY_CAP.
AUTHORITARIAN_UNHAPPY_PER_PCT = 0.5
AUTHORITARIAN_UNHAPPY_CAP = 15.0

# Egalitarian: national happiness bonus when control is uniform.
# bonus = UNIFORMITY_BONUS * (1 - stdev(province_controls) / 50)
# Max when all provinces have identical control; diminishes with variance.
EGALITARIAN_UNIFORMITY_BONUS = 8.0

# ---------------------------------------------------------------------------
# Rebellion Trigger Thresholds
# ---------------------------------------------------------------------------
# All three conditions must be true simultaneously to trigger a rebellion.
REBELLION_STABILITY_THRESHOLD = 20.0        # local_stability must be below this
REBELLION_HAPPINESS_THRESHOLD = 20.0        # local_happiness must be below this
REBELLION_IDEOLOGY_MISMATCH_THRESHOLD = 0.5 # compute_ideology_mismatch() must exceed this

# ---------------------------------------------------------------------------
# Rebel Timer
# ---------------------------------------------------------------------------
# When a province is rebel-occupied, the nation has this many turns to
# suppress the rebellion before the rebels accomplish their objective.
REBEL_TIMER_MIN = 3
REBEL_TIMER_MAX = 5

# ---------------------------------------------------------------------------
# Rebel Unit Sizing
# ---------------------------------------------------------------------------
# Rebel quantity spawned = population * rate, minimum 1.
REBEL_UNITS_PER_POP = 0.002  # 2 rebels per 1000 population

# ---------------------------------------------------------------------------
# Rebellion Outcomes
# ---------------------------------------------------------------------------
# When the rebel timer expires without suppression, one of three outcomes
# is chosen via weighted random selection.
OUTCOME_WHITESPACE = "whitespace"
OUTCOME_JOIN_NEIGHBOR = "join_neighbor"
OUTCOME_INDEPENDENCE = "independence"

# Base weights: whitespace most likely (safe default), independence rarest.
OUTCOME_BASE_WEIGHTS = {
    OUTCOME_WHITESPACE: 3,
    OUTCOME_JOIN_NEIGHBOR: 2,
    OUTCOME_INDEPENDENCE: 1,
}

# If an adjacent nation's ideology mismatch with the rebel province is below
# this threshold, add NEIGHBOR_WEIGHT_BONUS to the join_neighbor weight.
NEIGHBOR_IDEOLOGY_MATCH_THRESHOLD = 0.3
NEIGHBOR_WEIGHT_BONUS = 3

# ---------------------------------------------------------------------------
# Whitespace Rebel Spawning
# ---------------------------------------------------------------------------
# Probability per turn that a whitespace province with militarist or
# nationalist traits spawns a rebel formation.
WHITESPACE_REBEL_SPAWN_CHANCE = 0.02          # 2% per turn (~once per 4 years)
WHITESPACE_REBEL_UNITS_PER_POP = 0.001        # 1 rebel per 1000 population

# ---------------------------------------------------------------------------
# Partisan Stub
# ---------------------------------------------------------------------------
# Partisan rebels spawn in enemy-occupied provinces. Not yet implemented;
# requires the Occupation System.
PARTISAN_SPAWN_ENABLED = False
