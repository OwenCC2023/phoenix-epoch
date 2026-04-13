"""
Whitespace System constants.

Whitespace provinces are those with nation=None — outside national control.
They have stable populations, slowly shifting ideologies, and can influence
or be influenced by adjacent provinces.
"""

# ---------------------------------------------------------------------------
# De-integration (reverse normalization)
# ---------------------------------------------------------------------------

# When a province leaves a nation (collapse, cession), national ideology
# influence fades over this many turns. Shorter than integration (120)
# because ideology erodes faster without institutional reinforcement.
BASE_DEINTEGRATION_TURNS = 60  # 5 years

# ---------------------------------------------------------------------------
# Cross-provincial ideological melding
# ---------------------------------------------------------------------------

# Probability per turn that a whitespace province's ideology is pulled
# toward a dominant adjacent whitespace province.  With 3–5 neighbors,
# a province might experience melding roughly once per 6 months.
MELDING_RATE = 1.0 / 24  # ~once per 2 years per adjacency pair

# A province is susceptible to cultural pull only when its population is
# below this fraction of the neighbor's population.  Equal-pop neighbors
# reach cultural equilibrium and neither pulls the other.
MELDING_POP_DOMINANCE_RATIO = 0.5

# Probability that the strong trait slot is adopted from the dominant
# neighbor when melding fires.  Strong traits are stickier.
MELDING_STRONG_WEIGHT = 0.6

# Probability that a single weak trait slot is adopted from the dominant
# neighbor when melding fires.  Two weak slots = two independent rolls.
MELDING_WEAK_WEIGHT = 0.2

# ---------------------------------------------------------------------------
# Future system stubs
# ---------------------------------------------------------------------------

# Set True when the International Migration System is built.
# When enabled, whitespace populations will participate in migration flows.
WHITESPACE_MIGRATION_ENABLED = False

# Set True when the Control and Rebellion System is built.
# When enabled, provinces with these traits will be checked for rebel spawning.
REBEL_SPAWNING_ENABLED = False
REBEL_SPAWN_TRAITS = frozenset({"militarist", "nationalist"})
