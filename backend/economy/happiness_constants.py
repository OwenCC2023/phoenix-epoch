"""
Constants for the Happiness System.

Province.local_happiness is a 0-100 metric computed fresh each turn.
Base is 50. Source: trait-policy alignment (see happiness_policy_data.py) + trait baselines.

Downstream effects (all linear, centred at 50):
  Worker Productivity:      0.8× at 0  →  1.0× at 50  →  1.2× at 100
  Growth/turn (provincial): 0.9× at 0  →  1.0× at 50  →  1.1× at 100
  Stability Recovery/turn:  0.9× at 0  →  1.0× at 50  →  1.1× at 100
  Corruption Resistance:    stub — awaiting corruption system
"""

BASE_HAPPINESS = 50.0

# Scales the raw trait-policy sum to happiness points.
# A perfectly-aligned nation may accumulate a raw sum of ±40–80 across all
# policies; scaling by 0.5 keeps the resulting happiness change within ±20–40.
HAPPINESS_POLICY_SCALE = 0.5

# Trait weights for matrix scoring
HAPPINESS_STRONG_WEIGHT = 1.0
HAPPINESS_WEAK_WEIGHT = 0.5

# --- Downstream multiplier curves (linear) ---

# Worker Productivity: output × (0.8 + happiness × 0.004)
#   0 → 0.8,  50 → 1.0,  100 → 1.2
HAPPINESS_WORKER_PRODUCTIVITY_SLOPE = 0.004
HAPPINESS_WORKER_PRODUCTIVITY_BASE = 0.8

# Growth multiplier: rate × (0.9 + happiness × 0.002)
#   0 → 0.9,  50 → 1.0,  100 → 1.1
HAPPINESS_GROWTH_MULTIPLIER_SLOPE = 0.002
HAPPINESS_GROWTH_MULTIPLIER_BASE = 0.9

# Stability recovery multiplier: recovery × (0.9 + happiness × 0.002)
#   0 → 0.9,  50 → 1.0,  100 → 1.1
HAPPINESS_STABILITY_RECOVERY_MULTIPLIER_SLOPE = 0.002
HAPPINESS_STABILITY_RECOVERY_MULTIPLIER_BASE = 0.9
