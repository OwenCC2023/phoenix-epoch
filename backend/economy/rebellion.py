"""
Control, Regions, and Rebellion System — rebellion mechanics.

When a province is sufficiently unstable, unhappy, and ideologically opposed
to its nation, rebel forces spawn and occupy it. The nation then has a short
window to suppress the rebellion (via combat) before the rebels accomplish
their objective — which may be to revert to whitespace, join a neighboring
nation, or declare independence as a new NPC nation.

Key state on Province:
    is_rebel_occupied       — True while rebels hold the province
    rebel_timer_start_turn  — turn rebels spawned
    rebel_timer_duration    — how many turns the nation has (3–5, random)
"""

import random

from .control_constants import (
    REBELLION_STABILITY_THRESHOLD,
    REBELLION_HAPPINESS_THRESHOLD,
    REBELLION_IDEOLOGY_MISMATCH_THRESHOLD,
    REBEL_TIMER_MIN,
    REBEL_TIMER_MAX,
    REBEL_UNITS_PER_POP,
    OUTCOME_WHITESPACE,
    OUTCOME_JOIN_NEIGHBOR,
    OUTCOME_INDEPENDENCE,
    OUTCOME_BASE_WEIGHTS,
    NEIGHBOR_IDEOLOGY_MATCH_THRESHOLD,
    NEIGHBOR_WEIGHT_BONUS,
    WHITESPACE_REBEL_SPAWN_CHANCE,
    WHITESPACE_REBEL_UNITS_PER_POP,
    PARTISAN_SPAWN_ENABLED,
)


# ---------------------------------------------------------------------------
# Rebellion trigger
# ---------------------------------------------------------------------------

def check_rebellion_trigger(province, nation) -> bool:
    """Return True if the province meets all three rebellion conditions.

    Conditions (all must be true):
    1. local_stability < REBELLION_STABILITY_THRESHOLD (20)
    2. local_happiness < REBELLION_HAPPINESS_THRESHOLD (20)
    3. ideology mismatch between province and nation > REBELLION_IDEOLOGY_MISMATCH_THRESHOLD (0.5)

    A province that is already rebel-occupied cannot trigger a second rebellion.
    """
    if province.is_rebel_occupied:
        return False

    if province.local_stability >= REBELLION_STABILITY_THRESHOLD:
        return False
    if province.local_happiness >= REBELLION_HAPPINESS_THRESHOLD:
        return False

    from .normalization import compute_ideology_mismatch
    mismatch = compute_ideology_mismatch(
        province.ideology_traits or {},
        nation.ideology_traits or {},
    )
    if mismatch <= REBELLION_IDEOLOGY_MISMATCH_THRESHOLD:
        return False

    return True


# ---------------------------------------------------------------------------
# Rebel formation spawning
# ---------------------------------------------------------------------------

def spawn_rebel_formation(province, turn_number: int):
    """Spawn a rebel Formation and MilitaryUnit in the province.

    Creates:
      - A Formation owned by the province's nation (so it appears in nation
        military tracking) with a name indicating its rebel status.
      - A MilitaryUnit of type "rebel" sized proportionally to province population.

    Sets province.is_rebel_occupied = True and starts the timer.
    Does NOT save the province — caller is responsible.

    Returns the created Formation.
    """
    from provinces.models import Formation, MilitaryUnit

    quantity = max(1, int(province.population * REBEL_UNITS_PER_POP))
    timer = random.randint(REBEL_TIMER_MIN, REBEL_TIMER_MAX)

    formation = Formation.objects.create(
        nation=province.nation,
        province=province,
        name=f"Rebel Forces — {province.name}",
        domain=Formation.Domain.ARMY,
        formation_type=Formation.FormationType.ACTIVE,
        effective_strength=quantity,
    )

    MilitaryUnit.objects.create(
        formation=formation,
        unit_type="rebel",
        quantity=quantity,
        is_active=True,
    )

    province.is_rebel_occupied = True
    province.rebel_timer_start_turn = turn_number
    province.rebel_timer_duration = timer

    return formation


# ---------------------------------------------------------------------------
# Rebel suppression check
# ---------------------------------------------------------------------------

def check_rebel_suppression(province) -> bool:
    """Check whether the nation has suppressed the rebellion.

    Suppression stub: returns True if any non-rebel active formation in the
    province has effective_strength greater than the total rebel strength.
    Full combat resolution is deferred to the combat system.

    When the combat system is built, this function should be replaced or
    augmented with the actual combat resolution call.
    """
    from provinces.models import Formation

    rebel_formations = Formation.objects.filter(
        province=province,
        name__startswith="Rebel Forces",
    )
    rebel_strength = sum(f.effective_strength for f in rebel_formations)

    suppressor = Formation.objects.filter(
        province=province,
        nation=province.nation,
        formation_type=Formation.FormationType.ACTIVE,
    ).exclude(
        name__startswith="Rebel Forces"
    ).filter(
        effective_strength__gt=rebel_strength
    ).first()

    return suppressor is not None


# ---------------------------------------------------------------------------
# Rebellion resolution helpers
# ---------------------------------------------------------------------------

def _clear_rebel_state(province) -> None:
    """Clear rebel occupation state from a province. Does NOT save."""
    from provinces.models import Formation

    # Delete any rebel formations in this province
    Formation.objects.filter(
        province=province,
        name__startswith="Rebel Forces",
    ).delete()

    province.is_rebel_occupied = False
    province.rebel_timer_start_turn = None
    province.rebel_timer_duration = None


def _find_best_neighbor_nation(province):
    """Find the adjacent nation with the best ideology match for the rebel province.

    Returns a Nation if any adjacent nation's ideology mismatch is below
    NEIGHBOR_IDEOLOGY_MATCH_THRESHOLD, else returns None.
    """
    from .normalization import compute_ideology_mismatch

    province_traits = province.ideology_traits or {}
    best_nation = None
    best_mismatch = NEIGHBOR_IDEOLOGY_MATCH_THRESHOLD

    adjacent_nations = set()
    for adj in province.adjacent_provinces.select_related("nation").all():
        if adj.nation and adj.nation != province.nation and adj.nation.is_alive:
            adjacent_nations.add(adj.nation)

    for nation in adjacent_nations:
        mismatch = compute_ideology_mismatch(province_traits, nation.ideology_traits or {})
        if mismatch < best_mismatch:
            best_mismatch = mismatch
            best_nation = nation

    return best_nation


def _create_npc_nation(province) -> object:
    """Create an independent NPC nation from a rebel province.

    The NPC nation inherits the province's ideology and takes a generic
    government configuration. No player is assigned (player=None, is_npc=True).

    Returns the new Nation.
    """
    from nations.models import Nation

    npc = Nation.objects.create(
        game=province.game,
        player=None,
        is_npc=True,
        name=f"Free State of {province.name}",
        ideology_traits=province.ideology_traits or {},
        is_alive=True,
    )
    return npc


def resolve_rebel_victory(province, turn_number: int) -> str:
    """Resolve a rebellion that the nation failed to suppress in time.

    Selects an outcome via weighted random:
      - whitespace: province reverts to whitespace (release_single_province)
      - join_neighbor: province joins the most ideologically-aligned adjacent nation
      - independence: province forms a new NPC nation

    The join_neighbor weight is boosted if a good ideological match is found.
    Falls back to whitespace if join_neighbor is selected but no match exists.

    Returns the outcome string (OUTCOME_*).
    """
    from .whitespace import release_nation_provinces

    # Determine weights
    weights = dict(OUTCOME_BASE_WEIGHTS)
    best_neighbor = _find_best_neighbor_nation(province)
    if best_neighbor is not None:
        weights[OUTCOME_JOIN_NEIGHBOR] += NEIGHBOR_WEIGHT_BONUS

    outcomes = list(weights.keys())
    outcome_weights = [weights[o] for o in outcomes]
    chosen = random.choices(outcomes, weights=outcome_weights, k=1)[0]

    _clear_rebel_state(province)

    if chosen == OUTCOME_JOIN_NEIGHBOR:
        if best_neighbor is not None:
            # Transfer province to the neighboring nation
            old_nation = province.nation
            province.nation = best_neighbor
            province.is_core = False
            province.normalization_started_turn = turn_number
            from .normalization import get_normalization_duration
            province.normalization_duration = get_normalization_duration(best_neighbor)
            province.save()
            return OUTCOME_JOIN_NEIGHBOR
        else:
            # No match found — fall back to whitespace
            chosen = OUTCOME_WHITESPACE

    if chosen == OUTCOME_INDEPENDENCE:
        npc = _create_npc_nation(province)
        province.nation = npc
        province.is_core = True
        province.normalization_started_turn = None
        province.normalization_duration = None
        province.save()
        return OUTCOME_INDEPENDENCE

    # Default: whitespace
    old_nation = province.nation
    province.nation = None
    province.is_core = False
    province.deintegration_started_turn = turn_number
    from .whitespace_constants import BASE_DEINTEGRATION_TURNS
    province.deintegration_duration = BASE_DEINTEGRATION_TURNS
    province.save()
    return OUTCOME_WHITESPACE


# ---------------------------------------------------------------------------
# Per-nation rebellion tick
# ---------------------------------------------------------------------------

def process_rebellion_tick(provinces: list, nation, turn_number: int) -> None:
    """Run per-turn rebellion processing for all provinces of a nation.

    Steps:
    1. For non-rebel-occupied provinces: check trigger → spawn rebels.
    2. For rebel-occupied provinces: check suppression → clear if suppressed.
    3. For rebel-occupied provinces still mid-timer: check timer expiry → resolve.

    Provinces are modified in-place. The simulation loop must include the
    rebellion fields in Province.save(update_fields=[...]).
    """
    for province in provinces:
        if not province.is_rebel_occupied:
            # Step 1: check trigger
            if check_rebellion_trigger(province, nation):
                spawn_rebel_formation(province, turn_number)
            continue

        # Step 2: check suppression
        if check_rebel_suppression(province):
            _clear_rebel_state(province)
            continue

        # Step 3: check timer expiry
        if province.rebel_timer_start_turn is not None:
            elapsed = turn_number - province.rebel_timer_start_turn
            duration = province.rebel_timer_duration or REBEL_TIMER_MAX
            if elapsed >= duration:
                # Rebels win — resolve the outcome
                # Note: resolve_rebel_victory saves the province internally
                # and modifies province.nation, so we must NOT re-save it
                # in the outer simulation loop. Mark it for skip.
                resolve_rebel_victory(province, turn_number)


# ---------------------------------------------------------------------------
# Whitespace rebel spawning
# ---------------------------------------------------------------------------

def spawn_whitespace_rebels(province, turn_number: int) -> None:
    """Spawn rebels in a whitespace province with militarist/nationalist traits.

    Whitespace rebel bands are ownerless — no nation FK on the formation.
    They represent local armed groups that may harass nearby nations' border
    provinces (stub for future combat and occupation systems).

    Fires probabilistically at WHITESPACE_REBEL_SPAWN_CHANCE per turn.
    """
    from provinces.models import Formation, MilitaryUnit
    from .control_constants import WHITESPACE_REBEL_SPAWN_CHANCE, WHITESPACE_REBEL_UNITS_PER_POP

    if random.random() > WHITESPACE_REBEL_SPAWN_CHANCE:
        return

    quantity = max(1, int(province.population * WHITESPACE_REBEL_UNITS_PER_POP))

    formation = Formation.objects.create(
        nation=None,  # ownerless — whitespace rebel band
        province=province,
        name=f"Armed Band — {province.name}",
        domain=Formation.Domain.ARMY,
        formation_type=Formation.FormationType.ACTIVE,
        effective_strength=quantity,
    )

    MilitaryUnit.objects.create(
        formation=formation,
        unit_type="rebel",
        quantity=quantity,
        is_active=True,
    )


# ---------------------------------------------------------------------------
# Partisan stub
# ---------------------------------------------------------------------------

def spawn_partisan_rebels(province, turn_number: int) -> None:
    """Stub: partisan rebels in enemy-occupied provinces.

    No-op until the Occupation System is built. Set PARTISAN_SPAWN_ENABLED=True
    and implement occupation tracking to activate this.
    """
    if not PARTISAN_SPAWN_ENABLED:
        return
    # Future implementation: check if province is enemy-occupied, spawn partisans
