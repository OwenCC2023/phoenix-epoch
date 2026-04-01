"""Espionage Attack, Defense, and Transparency computation.

All functions are pure — they accept pre-fetched data and return computed
values without touching the database. This keeps the logic testable and
the simulation loop in control of DB reads/writes.
"""

from .constants import (
    ESPIONAGE_ATTACK_POLICY_MODIFIERS,
    ESPIONAGE_DEFENSE_POLICY_MODIFIERS,
    ESPIONAGE_TRAIT_MODIFIERS,
    STABILITY_ATTACK_BREAKPOINTS,
    STABILITY_DEFENSE_BREAKPOINTS,
    LITERACY_DEFENSE_BREAKPOINTS,
)


# ---------------------------------------------------------------------------
# Breakpoint helpers
# ---------------------------------------------------------------------------

def _breakpoint_bonus(advantage, breakpoints):
    """Return the bonus for a given advantage using descending breakpoints.

    Breakpoints are sorted largest-first: [(30, 10), (20, 7), (10, 4), (5, 2)].
    The first threshold that the advantage meets or exceeds determines the bonus.
    """
    for threshold, bonus in breakpoints:
        if advantage >= threshold:
            return bonus
    return 0


# ---------------------------------------------------------------------------
# Trait modifier helpers
# ---------------------------------------------------------------------------

def _get_trait_attack(ideology_traits):
    """Sum flat attack bonuses from ideology traits."""
    total = 0
    strong = ideology_traits.get("strong", "")
    weak_list = ideology_traits.get("weak", [])

    if strong in ESPIONAGE_TRAIT_MODIFIERS:
        total += ESPIONAGE_TRAIT_MODIFIERS[strong]["attack"]["strong"]
    for trait in weak_list:
        if trait in ESPIONAGE_TRAIT_MODIFIERS:
            total += ESPIONAGE_TRAIT_MODIFIERS[trait]["attack"]["weak"]
    return total


def _get_trait_defense(ideology_traits):
    """Sum flat defense bonuses from ideology traits."""
    total = 0
    strong = ideology_traits.get("strong", "")
    weak_list = ideology_traits.get("weak", [])

    if strong in ESPIONAGE_TRAIT_MODIFIERS:
        total += ESPIONAGE_TRAIT_MODIFIERS[strong]["defense"]["strong"]
    for trait in weak_list:
        if trait in ESPIONAGE_TRAIT_MODIFIERS:
            total += ESPIONAGE_TRAIT_MODIFIERS[trait]["defense"]["weak"]
    return total


# ---------------------------------------------------------------------------
# National Attack
# ---------------------------------------------------------------------------

def compute_national_attack(
    fia_policy_level,
    building_attack,
    espionage_bonus,
    ideology_traits,
    stability_advantage,
):
    """Compute a nation's espionage attack value against a specific target.

    Args:
        fia_policy_level: Current level of the foreign_intelligence_agency policy (0-3).
            Level 0 (Nonexistent) forces attack to zero — hard gate.
        building_attack: Sum of espionage_attack from national building effects.
        espionage_bonus: Fractional bonus from traits + policies (e.g. 0.25 from Devious).
        ideology_traits: Nation's ideology_traits dict {"strong": ..., "weak": [...]}.
        stability_advantage: own_stability - target_stability (can be negative).

    Returns:
        float: National attack value (>= 0).
    """
    # Hard gate: FIA nonexistent = no espionage capability
    fia_attack = ESPIONAGE_ATTACK_POLICY_MODIFIERS.get(
        "foreign_intelligence_agency", {}
    ).get(fia_policy_level)
    if fia_attack is None:
        return 0.0

    base = building_attack + fia_attack
    base += _get_trait_attack(ideology_traits)

    # Multiplicative scaling from existing espionage_bonus stub
    base *= (1.0 + espionage_bonus)

    # Stability advantage (only positive relative stability gives a bonus)
    if stability_advantage > 0:
        base += _breakpoint_bonus(stability_advantage, STABILITY_ATTACK_BREAKPOINTS)

    return max(0.0, base)


# ---------------------------------------------------------------------------
# National Defense
# ---------------------------------------------------------------------------

def compute_national_defense(
    building_defense,
    counter_espionage_bonus,
    active_policies,
    ideology_traits,
    stability_advantage,
    literacy_advantage=0,
):
    """Compute a nation's espionage defense value against a specific attacker.

    Args:
        building_defense: Sum of espionage_defense from national building effects.
        counter_espionage_bonus: Fractional bonus from traits + policies.
        active_policies: Dict of {policy_category: current_level} for the defending nation.
        ideology_traits: Nation's ideology_traits dict.
        stability_advantage: own_stability - attacker_stability.
        literacy_advantage: own_literacy - attacker_literacy (stub, default 0).

    Returns:
        float: National defense value (>= 0).
    """
    base = building_defense

    # Policy defense modifiers
    for cat, level_map in ESPIONAGE_DEFENSE_POLICY_MODIFIERS.items():
        level = active_policies.get(cat)
        if level is not None and level in level_map:
            base += level_map[level]

    # Trait defense modifiers
    base += _get_trait_defense(ideology_traits)

    # Multiplicative scaling from existing counter_espionage_bonus stub
    base *= (1.0 + counter_espionage_bonus)

    # Stability advantage
    if stability_advantage > 0:
        base += _breakpoint_bonus(stability_advantage, STABILITY_DEFENSE_BREAKPOINTS)

    # Literacy advantage (stub — will fire when literacy system is wired)
    if literacy_advantage > 0:
        base += _breakpoint_bonus(literacy_advantage, LITERACY_DEFENSE_BREAKPOINTS)

    return max(0.0, base)


# ---------------------------------------------------------------------------
# Provincial Defense
# ---------------------------------------------------------------------------

def compute_provincial_defense(national_defense, provincial_bldg_defense, suppress_bonus=0):
    """Compute effective defense for a specific province.

    Args:
        national_defense: Nation's computed national defense.
        provincial_bldg_defense: Sum of provincial_espionage_defense from province buildings.
        suppress_bonus: Bonus from active suppress_foreign_operations actions on this province.

    Returns:
        float: Provincial defense value.
    """
    return national_defense + provincial_bldg_defense + suppress_bonus


# ---------------------------------------------------------------------------
# Transparency
# ---------------------------------------------------------------------------

def compute_transparency(attack, defense):
    """Compute transparency as the fraction by which attack exceeds defense.

    Per the design doc: transparency is "the percentage by which infiltrator
    National Attack dwarfs target National Defense". Minimum zero.

    Args:
        attack: Effective attack value.
        defense: Effective defense value.

    Returns:
        float: Transparency in [0.0, 1.0].
    """
    if defense <= 0:
        return 1.0 if attack > 0 else 0.0
    if attack <= defense:
        return 0.0
    return min(1.0, (attack - defense) / defense)
