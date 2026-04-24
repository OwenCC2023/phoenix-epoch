"""
Literacy system constants.

Province.literacy is a 0.0–1.0 metric (fraction of literate population).
Starting value: 0.20 (20%).

Growth operates on an S-curve: slow at low and high literacy, fastest near 50%.
Formula: growth = BASE_LITERACY_GROWTH * literacy * (1 - literacy) * 4 * modifiers
The *4 normalises the curve so peak growth (at literacy=0.5) equals BASE_LITERACY_GROWTH.

Calibration:
  At 20% literacy: effective_base = 0.005 * 0.2 * 0.8 * 4 ≈ 0.0032/month → ~3.8%/year
  At 50% literacy: effective_base = 0.005 * 0.5 * 0.5 * 4 = 0.005/month  → ~6.0%/year
  At 80% literacy: effective_base = 0.005 * 0.8 * 0.2 * 4 ≈ 0.0032/month → ~3.8%/year
  Time from 20% to 80% (no modifiers): ~120 turns (10 years).
"""

# Base growth rate per turn — the peak of the S-curve (at literacy 50%).
BASE_LITERACY_GROWTH = 0.005

# ---------------------------------------------------------------------------
# Kapital contribution to literacy growth
# ---------------------------------------------------------------------------

# Kapital per capita at which the kapital bonus is 100% (doubles growth).
KAPITAL_LITERACY_SCALE = 5.0

# Maximum kapital bonus to literacy growth (additive fraction, e.g. 0.5 = +50%).
KAPITAL_LITERACY_CAP = 0.5

# ---------------------------------------------------------------------------
# Population growth dilution
# ---------------------------------------------------------------------------

# Pop growth rate above which rapid population growth dilutes literacy.
# Each 0.1%/month above this threshold reduces literacy growth.
POP_GROWTH_DILUTION_THRESHOLD = 0.003  # 0.3%/month

# Fraction of excess pop growth that reduces literacy growth.
POP_GROWTH_DILUTION_FACTOR = 0.5

# ---------------------------------------------------------------------------
# Policy penalties on literacy growth
# ---------------------------------------------------------------------------

# child_labor levels: 0=illegal, 1=regulated, 2=unrestricted, 3=unrestricted+child_soldiers
# These reduce literacy growth as a multiplier (additive to 1.0).
# Never drives growth negative on their own.
CHILD_LABOR_LITERACY_PENALTY = {
    0: 0.0,    # illegal — no penalty
    1: -0.15,  # regulated — mild negative; offsets some school benefits
    2: -0.40,  # unrestricted — negates Mandatory Primary Education
    3: -0.60,  # unrestricted + child soldiers — negates Mandatory Secondary Education
}

# slavery levels: 0=illegal, 1=rare, 2=common, 3=slave_society
# Growth penalty (additive to 1.0) — never drives growth negative on its own.
SLAVERY_LITERACY_GROWTH_PENALTY = {
    0: 0.0,
    1: -0.10,
    2: -0.25,
    3: -0.40,
}

# Hard cap on maximum literacy % by slavery level.
SLAVERY_LITERACY_CAP = {
    0: 1.0,   # illegal — no cap
    1: 0.90,  # rare — cap at 90%
    2: 0.70,  # common — cap at 70%
    3: 0.50,  # slave_society — cap at 50%
}

# ---------------------------------------------------------------------------
# Downstream effects
# ---------------------------------------------------------------------------

# Happiness amplification from literacy.
# final_happiness = BASE_HAPPINESS + raw_delta * (1.0 + literacy * LITERACY_HAPPINESS_AMPLIFIER)
# At 100% literacy: deltas are 1.5× as large (both positive and negative).
# At  20% literacy: deltas are 1.1× as large.
LITERACY_HAPPINESS_AMPLIFIER = 0.5

# Migration sensitivity from literacy.
# Literate pops are more likely to migrate to better conditions.
# outflow_rate *= (1.0 + province.literacy * LITERACY_MIGRATION_SENSITIVITY)
# At 100% literacy: 30% higher migration outflow.
LITERACY_MIGRATION_SENSITIVITY = 0.3
