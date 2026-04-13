"""
Whitespace System — simulation of provinces outside national control.

Whitespace provinces (nation=None) have stable populations and slowly shifting
ideologies. When a nation collapses, its provinces revert to whitespace,
retaining national ideology that fades through de-integration. Adjacent
whitespace provinces influence each other's ideologies through melding,
weighted by population dominance.

Key functions:
    simulate_all_whitespace()     — per-turn entry point (replaces old drift loop)
    initialize_whitespace()       — game-start setup
    release_nation_provinces()    — nation collapse handler
    assign_random_ideology()      — random valid ideology for a province
"""

import random

from .whitespace_constants import (
    BASE_DEINTEGRATION_TURNS,
    MELDING_RATE,
    MELDING_POP_DOMINANCE_RATIO,
    MELDING_STRONG_WEIGHT,
    MELDING_WEAK_WEIGHT,
    WHITESPACE_MIGRATION_ENABLED,
    REBEL_SPAWNING_ENABLED,
)
from .integration_constants import UNCLAIMED_DRIFT_RATE


# ---------------------------------------------------------------------------
# Random ideology assignment
# ---------------------------------------------------------------------------

def assign_random_ideology(province) -> None:
    """Pick 3 random trait pairs and assign 1 strong + 2 weak traits.

    Each trait slot comes from a different pair. The strong trait is a random
    choice within its pair; weak traits likewise.

    Mutates province.ideology_traits in place. Does NOT call province.save().
    """
    from nations.trait_constants import TRAIT_PAIRS

    pairs = list(TRAIT_PAIRS)
    random.shuffle(pairs)
    chosen = pairs[:3]

    strong = random.choice(chosen[0])
    weak = [random.choice(chosen[1]), random.choice(chosen[2])]

    province.ideology_traits = {"strong": strong, "weak": weak}


# ---------------------------------------------------------------------------
# Game-start initialization
# ---------------------------------------------------------------------------

def initialize_whitespace(game) -> None:
    """Set up all provinces at game start.

    - Whitespace provinces (nation=None): randomize population using the
      full terrain+relief+vegetation+temperature formula, assign random
      ideologies.
    - Owned provinces: override ideology_traits to match their nation's
      ideology (they start fully aligned).

    Called from GameStartView.post() after the game transitions to ACTIVE.
    """
    from provinces.models import Province, randomise_starting_population

    provinces = list(
        Province.objects.filter(game=game).select_related("nation")
    )

    whitespace_to_update = []
    owned_to_update = []

    for province in provinces:
        if province.nation is None:
            # Whitespace: randomize population and ideology.
            province.population = randomise_starting_population(
                province.terrain_type,
                relief=province.relief,
                vegetation_level=province.vegetation_level,
                temperature_band=province.temperature_band,
            )
            assign_random_ideology(province)
            whitespace_to_update.append(province)
        else:
            # Owned: align ideology to nation.
            province.ideology_traits = province.nation.ideology_traits or {}
            owned_to_update.append(province)

    if whitespace_to_update:
        Province.objects.bulk_update(
            whitespace_to_update,
            ["population", "ideology_traits"],
            batch_size=500,
        )
    if owned_to_update:
        Province.objects.bulk_update(
            owned_to_update,
            ["ideology_traits"],
            batch_size=500,
        )


# ---------------------------------------------------------------------------
# Nation collapse — release provinces to whitespace
# ---------------------------------------------------------------------------

def release_nation_provinces(nation, turn_number: int) -> None:
    """Release all provinces of a collapsed nation to whitespace.

    - Sets nation=None (whitespace).
    - Clears in-progress normalization.
    - Starts de-integration (ideology fade-out).
    - Preserves current ideology_traits (they were aligned to the nation;
      de-integration will gradually erode them).

    Called from TurnResolutionEngine._check_collapse_conditions() after
    nation.is_alive is set to False.
    """
    from provinces.models import Province

    provinces = list(Province.objects.filter(nation=nation))
    if not provinces:
        return

    for province in provinces:
        province.nation = None
        province.is_core = False
        province.normalization_started_turn = None
        province.normalization_duration = None
        province.deintegration_started_turn = turn_number
        province.deintegration_duration = BASE_DEINTEGRATION_TURNS

    Province.objects.bulk_update(
        provinces,
        [
            "nation",
            "is_core",
            "normalization_started_turn",
            "normalization_duration",
            "deintegration_started_turn",
            "deintegration_duration",
        ],
        batch_size=500,
    )


# ---------------------------------------------------------------------------
# De-integration (reverse normalization)
# ---------------------------------------------------------------------------

def _deintegrate_province(province, turn_number: int) -> bool:
    """Process one turn of de-integration for a province.

    De-integration represents the gradual erosion of national ideology after
    a province leaves a nation. Early on, the ideology is sticky (the
    population still remembers). As time passes, drift probability increases.

    Returns True if ideology_traits was modified this turn.
    """
    from nations.trait_constants import TRAIT_PAIRS, TRAIT_DEFS

    if province.deintegration_started_turn is None:
        return False

    duration = province.deintegration_duration or BASE_DEINTEGRATION_TURNS
    elapsed = turn_number - province.deintegration_started_turn

    if elapsed >= duration:
        # De-integration complete — province is now native whitespace.
        province.deintegration_started_turn = None
        province.deintegration_duration = None
        return False

    # Drift probability increases over time: starts near 0, ends near
    # 3× the base unclaimed drift rate. This means recently-released
    # provinces are ideologically stable, but the influence erodes.
    progress = elapsed / max(1, duration)
    drift_chance = progress * UNCLAIMED_DRIFT_RATE * 3.0

    if random.random() > drift_chance:
        return False

    # Drift one random trait slot toward a random valid alternative.
    return _drift_one_trait_slot(province, TRAIT_PAIRS, TRAIT_DEFS)


def _drift_one_trait_slot(province, trait_pairs, trait_defs) -> bool:
    """Shift one random ideology trait slot to a random valid alternative.

    Ensures the 3-slot constraint (all from different pairs) is maintained.
    Returns True if a change was made.
    """
    current = province.ideology_traits or {}
    strong = current.get("strong")
    weak_list = list(current.get("weak", []))

    if not strong and not weak_list:
        # No ideology to drift — assign a fresh one instead.
        assign_random_ideology(province)
        return True

    slot = random.randint(0, 2)  # 0=strong, 1=weak[0], 2=weak[1]

    if slot == 0 and strong:
        current_pair_idx = trait_defs.get(strong, {}).get("pair_index", -1)
        candidates = [
            t for t in trait_defs
            if trait_defs[t].get("pair_index") != current_pair_idx
        ]
        if candidates:
            province.ideology_traits = {
                "strong": random.choice(candidates),
                "weak": weak_list,
            }
            return True
    elif 1 <= slot <= 2 and len(weak_list) > slot - 1:
        idx = slot - 1
        current_weak = weak_list[idx]
        current_pair_idx = trait_defs.get(current_weak, {}).get("pair_index", -1)
        # Must not reuse the pair of the strong trait or the other weak trait.
        used_pairs = {
            trait_defs.get(strong, {}).get("pair_index", -1),
            trait_defs.get(
                weak_list[1 - idx] if len(weak_list) > 1 - idx else None, {}
            ).get("pair_index", -1),
            current_pair_idx,
        }
        candidates = [
            t for t in trait_defs
            if trait_defs[t].get("pair_index") not in used_pairs
        ]
        if candidates:
            new_weak = list(weak_list)
            new_weak[idx] = random.choice(candidates)
            province.ideology_traits = {"strong": strong, "weak": new_weak}
            return True

    return False


# ---------------------------------------------------------------------------
# Cross-provincial ideological melding
# ---------------------------------------------------------------------------

def _compute_ideology_melding(province, adjacent_whitespace: list) -> bool:
    """Influence this province's ideology based on dominant adjacent provinces.

    A province is susceptible to cultural pull when its population is below
    MELDING_POP_DOMINANCE_RATIO of a neighbor's population. When melding
    fires, one trait slot from the dominant neighbor is adopted (respecting
    trait-pair constraints).

    Parameters
    ----------
    province : Province
        The whitespace province to potentially modify.
    adjacent_whitespace : list[Province]
        Adjacent provinces that are also whitespace (pre-filtered by caller).

    Returns True if ideology_traits was modified.
    """
    from nations.trait_constants import TRAIT_DEFS

    if not adjacent_whitespace:
        return False

    # Find the most dominant neighbor (highest population that dominates us).
    dominant = None
    for neighbor in adjacent_whitespace:
        if province.population < neighbor.population * MELDING_POP_DOMINANCE_RATIO:
            if dominant is None or neighbor.population > dominant.population:
                dominant = neighbor

    if dominant is None:
        return False

    # Roll for melding.
    if random.random() > MELDING_RATE:
        return False

    # Attempt to adopt one trait slot from the dominant neighbor.
    neighbor_traits = dominant.ideology_traits or {}
    province_traits = province.ideology_traits or {}

    if not neighbor_traits or not province_traits:
        return False

    n_strong = neighbor_traits.get("strong")
    n_weak = list(neighbor_traits.get("weak", []))
    p_strong = province_traits.get("strong")
    p_weak = list(province_traits.get("weak", []))

    if len(p_weak) < 2 or len(n_weak) < 2:
        return False

    # Try each slot randomly with its weight.
    slots = [0, 1, 2]
    random.shuffle(slots)

    for slot in slots:
        if slot == 0:
            # Strong slot adoption.
            if random.random() > MELDING_STRONG_WEIGHT:
                continue
            if n_strong and n_strong != p_strong:
                # Check pair constraint: new strong must not share pair with
                # either weak.
                n_strong_pair = TRAIT_DEFS.get(n_strong, {}).get("pair_index", -1)
                weak_pairs = {
                    TRAIT_DEFS.get(p_weak[0], {}).get("pair_index", -2),
                    TRAIT_DEFS.get(p_weak[1], {}).get("pair_index", -3),
                }
                if n_strong_pair not in weak_pairs:
                    province.ideology_traits = {
                        "strong": n_strong,
                        "weak": p_weak,
                    }
                    return True
        else:
            # Weak slot adoption.
            if random.random() > MELDING_WEAK_WEIGHT:
                continue
            idx = slot - 1
            n_trait = n_weak[idx] if idx < len(n_weak) else None
            if n_trait and n_trait != p_weak[idx]:
                # Check pair constraint: new weak must not share pair with
                # strong or the other weak.
                n_trait_pair = TRAIT_DEFS.get(n_trait, {}).get("pair_index", -1)
                used_pairs = {
                    TRAIT_DEFS.get(p_strong, {}).get("pair_index", -2),
                    TRAIT_DEFS.get(
                        p_weak[1 - idx], {}
                    ).get("pair_index", -3),
                }
                if n_trait_pair not in used_pairs:
                    new_weak = list(p_weak)
                    new_weak[idx] = n_trait
                    province.ideology_traits = {
                        "strong": p_strong,
                        "weak": new_weak,
                    }
                    return True

    return False


# ---------------------------------------------------------------------------
# Per-province simulation tick
# ---------------------------------------------------------------------------

def _simulate_whitespace_province(
    province, turn_number: int, adjacent_whitespace: list
) -> set:
    """Run one turn of whitespace simulation for a single province.

    Steps:
        1. De-integration (if active — recently left a nation).
        2. Cross-provincial ideological melding.
        3. Random ideology drift (only if NOT de-integrating — de-integration
           handles its own drift).
        4. Stubs for future migration and rebel spawning.

    Returns the set of field names that were modified (for update_fields).
    """
    from .normalization import drift_unclaimed_ideology

    modified = set()

    # Step 1: De-integration.
    is_deintegrating = province.deintegration_started_turn is not None
    if is_deintegrating:
        if _deintegrate_province(province, turn_number):
            modified.add("ideology_traits")
        # Always track deintegration field changes (completion clears them).
        modified.add("deintegration_started_turn")
        modified.add("deintegration_duration")

    # Step 2: Melding — only if de-integration didn't already change ideology.
    if "ideology_traits" not in modified:
        if _compute_ideology_melding(province, adjacent_whitespace):
            modified.add("ideology_traits")

    # Step 3: Random drift — only if not de-integrating and melding didn't fire.
    if not is_deintegrating and "ideology_traits" not in modified:
        old_traits = province.ideology_traits
        drift_unclaimed_ideology(province)
        if province.ideology_traits != old_traits:
            modified.add("ideology_traits")

    # Step 4: Rebel spawning for militarist/nationalist whitespace provinces.
    if REBEL_SPAWNING_ENABLED:
        province_traits = province.ideology_traits or {}
        trait_keys = set()
        if province_traits.get("strong"):
            trait_keys.add(province_traits["strong"])
        trait_keys.update(province_traits.get("weak", []))
        if trait_keys & REBEL_SPAWN_TRAITS:
            from .rebellion import spawn_whitespace_rebels
            spawn_whitespace_rebels(province, turn_number)

    # Step 5: Future stubs.
    # if WHITESPACE_MIGRATION_ENABLED:
    #     pass  # future: whitespace migration

    return modified


# ---------------------------------------------------------------------------
# Game-wide whitespace simulation — entry point
# ---------------------------------------------------------------------------

def simulate_all_whitespace(game, turn_number: int) -> None:
    """Simulate all whitespace provinces for one turn.

    Replaces the old unclaimed-province drift loop in
    simulate_economy_for_game(). Queries all nation=None provinces,
    builds an adjacency lookup, and runs the per-province simulation.
    """
    from provinces.models import Province

    unclaimed = list(
        Province.objects.filter(game=game, nation__isnull=True)
        .prefetch_related("adjacent_provinces")
    )

    if not unclaimed:
        return

    # Build a set of whitespace province IDs for fast adjacency filtering.
    whitespace_ids = {p.id for p in unclaimed}

    # Build an ID→province lookup for resolving adjacencies.
    province_by_id = {p.id: p for p in unclaimed}

    to_save = []

    for province in unclaimed:
        # Filter adjacent provinces to only those that are also whitespace.
        adjacent_whitespace = [
            province_by_id[adj.id]
            for adj in province.adjacent_provinces.all()
            if adj.id in whitespace_ids
        ]

        modified = _simulate_whitespace_province(
            province, turn_number, adjacent_whitespace
        )

        if modified:
            to_save.append((province, list(modified)))

    # Save modified provinces individually with targeted update_fields
    # to avoid overwriting concurrent changes from nation simulation.
    for province, fields in to_save:
        province.save(update_fields=fields)
