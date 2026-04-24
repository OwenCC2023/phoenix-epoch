"""Constants for the Tax Efficiency (TE) calculation.

TE is the fraction of the stated tax rate actually collected.  Range [0.01, 1.0].

Calibrated so that with all efficient traits + max buildings + efficient gov:
    0.44 + 0.09 + 0.06 + 0.06 + 0.06 + 0.05 + 0.05 + 0.05 + 0.14 = 1.00
And with all inefficient traits + no buildings + inefficient gov:
    0.44 − 0.09 − 0.06 − 0.06 − 0.06 − 0.05 − 0.06 − 0.05 = 0.01

Government modifiers live in nations.government_constants (per-axis `tax_efficiency`
entries) and are summed via get_combined_government_effects().
Trait modifiers live in nations.trait_constants (`tax_efficiency` key in strong/weak
effects) and are merged via get_effective_trait_effects().

This module holds only the base, building-bonus, and clamp constants.
"""

TE_BASE = 0.44

# Hard clamps — TE never goes below 0.01 or above 1.0.
TE_MIN = 0.01
TE_MAX = 1.0

# Per-province building bonus parameters.
TE_BUILDING_CATEGORIES = (
    "government_regulatory",
    "government_management",
    "government_oversight",
)
TE_BUILDING_BONUS_PER_LEVEL = 0.02
TE_BUILDING_BONUS_MAX = 0.14
