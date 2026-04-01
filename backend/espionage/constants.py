"""Espionage system constants and balance parameters.

All flat additive values are on the same scale as Attack/Defense scores
(roughly 0–80 range for a typical nation).
"""

# ---------------------------------------------------------------------------
# Defense policy modifiers — flat additive contribution to National Defense
# ---------------------------------------------------------------------------
# Key = policy category, value = {level_index: defense_modifier}
# "Base" level noted in comments; a neutral policy loadout sums to ~0.

ESPIONAGE_DEFENSE_POLICY_MODIFIERS = {
    # Policing: more institutional = more defense.  Base: Town Watch (1)
    # Level 2 "Corrupt" is worse than no police — corrupt cops undermine defense.
    "policing": {0: -8, 1: -3, 2: -5, 3: 4, 4: 6, 5: 8},

    # Anti-corruption: lower penalties = less defense.  Base: Zero Tolerance (3)
    "anti_corruption_policy": {0: -6, 1: -3, 2: 3, 3: 5},

    # Visa: more stringent = more defense.  Base: Visa on Arrival (3)
    "visa_policy": {0: 6, 1: 4, 2: 2, 3: 0, 4: -5},

    # Naturalization: more stringent = more defense.  Base: 4-7 Years (2)
    "naturalization_laws": {0: -6, 1: -3, 2: 0, 3: 2, 4: 3, 5: 4, 6: 6},

    # Domestic intel: nonexistent = massive defense loss.
    "domestic_intelligence_agency": {0: -15, 1: 2, 2: 6, 3: 10},

    # Freedom of movement: fewer restrictions = less defense.  Base: Elites Only (2)
    "freedom_of_movement": {0: -5, 1: -2, 2: 0, 3: 4},

    # Freedom of association: fewer restrictions = less defense.  Base: Approved Orgs (1)
    "freedom_of_association": {0: -5, 1: 0, 2: -2, 3: 4},

    # Gender rights: more rights = more defense.  Base: Homemakers (3)
    "gender_rights": {0: 4, 1: 2, 2: 0, 3: -3},

    # Racial rights: more rights = more defense.  Base: Exclusivity (0)
    "racial_rights": {0: -5, 1: -3, 2: -1, 3: 4},

    # Social discrimination: more discrimination = less defense.  Base: Minimal (4)
    "social_discrimination": {0: -8, 1: -5, 2: -3, 3: -1, 4: 0, 5: 3},
}

# ---------------------------------------------------------------------------
# Attack policy modifiers — flat additive contribution to National Attack
# ---------------------------------------------------------------------------
# Only foreign_intelligence_agency contributes.
# Level 0 (Nonexistent) is a hard gate: attack forced to zero.
# None sentinel means "gate to zero".

ESPIONAGE_ATTACK_POLICY_MODIFIERS = {
    "foreign_intelligence_agency": {0: None, 1: 5, 2: 10, 3: 18},
}

# ---------------------------------------------------------------------------
# Ideology trait modifiers — flat additive, keyed by trait name
# ---------------------------------------------------------------------------
# Each dict has "attack" and "defense" sub-dicts with "strong"/"weak" values.

ESPIONAGE_TRAIT_MODIFIERS = {
    "authoritarian": {"attack": {"strong": 0, "weak": 0}, "defense": {"strong": 6, "weak": 3}},
    "honorable":     {"attack": {"strong": 0, "weak": 0}, "defense": {"strong": 8, "weak": 4}},
    "devious":       {"attack": {"strong": 10, "weak": 5}, "defense": {"strong": -6, "weak": -3}},
    "libertarian":   {"attack": {"strong": 0, "weak": 0}, "defense": {"strong": -6, "weak": -3}},
}

# ---------------------------------------------------------------------------
# Relative stability breakpoints — (min_advantage, bonus)
# ---------------------------------------------------------------------------
# Only the side with HIGHER stability gets a bonus; the other gets nothing.

STABILITY_ATTACK_BREAKPOINTS = [
    (30, 10),
    (20, 7),
    (10, 4),
    (5, 2),
]

STABILITY_DEFENSE_BREAKPOINTS = [
    (30, 10),
    (20, 7),
    (10, 4),
    (5, 2),
]

# ---------------------------------------------------------------------------
# Relative literacy breakpoints — defense only (stub until literacy wired)
# ---------------------------------------------------------------------------

LITERACY_DEFENSE_BREAKPOINTS = [
    (20, 6),
    (10, 4),
    (5, 2),
]

# ---------------------------------------------------------------------------
# Building effect keys
# ---------------------------------------------------------------------------

ESPIONAGE_ATTACK_BUILDING_KEY = "espionage_attack"           # national scope
ESPIONAGE_DEFENSE_BUILDING_KEY = "espionage_defense"         # national scope
PROVINCIAL_DEFENSE_BUILDING_KEY = "provincial_espionage_defense"  # province scope

# ---------------------------------------------------------------------------
# Transparency information categories — ordered easiest to hardest
# ---------------------------------------------------------------------------

TRANSPARENCY_CATEGORIES = [
    "building_locations",
    "province_level_info",
    "positions_of_formations",
    "cointel",
    "foreign_espionage",
]

# Weight of each category in the total information pool
TRANSPARENCY_CATEGORY_WEIGHTS = {
    "building_locations": 0.30,
    "province_level_info": 0.25,
    "positions_of_formations": 0.20,
    "cointel": 0.15,
    "foreign_espionage": 0.10,
}

# ---------------------------------------------------------------------------
# Action definitions
# ---------------------------------------------------------------------------

FOREIGN_ACTION_TYPES = [
    "investigate_province",
    "promote_foreign_ideology",
    "terrorist_attack",
    "sabotage_building",
]

DOMESTIC_ACTION_TYPES = [
    "suppress_foreign_operations",
]

ESPIONAGE_ACTION_DEFS = {
    "investigate_province": {
        "type": "foreign",
        "attack_bonus": 30,       # massive per-province transparency boost
        "min_fia_level": 1,
        "duration": 1,            # turns
    },
    "promote_foreign_ideology": {
        "type": "foreign",
        "min_fia_level": 1,
        "duration": 3,
        "stability_per_turn": -2.0,
        "security_per_turn": -1.0,
        "extra_instability": -1.5,  # if happiness < 40 or security < 30
    },
    "terrorist_attack": {
        "type": "foreign",
        "min_fia_level": 2,
        "duration": 1,
        "pop_kill_fraction": 0.002,
        "security_penalty": -20.0,
        "security_penalty_duration": 3,  # turns
    },
    "sabotage_building": {
        "type": "foreign",
        "min_fia_level": 2,
        "duration": 1,
        "base_disable_turns": 2,
        "transparency_disable_scale": 3,  # disable = base + scale * transparency
    },
    "suppress_foreign_operations": {
        "type": "domestic",
        "defense_bonus": 15,
        "min_dia_level": 1,
        "duration": None,         # persistent until cancelled
    },
}
