"""
Provincial Integration System — normalization computation.

When a non-core province joins a nation it carries its own ideology traits.
Over a normalization period these drift toward the national ideology, causing
stability and happiness penalties that diminish linearly as alignment improves.

After normalization completes the province becomes a core province and behaves
identically to all others.
"""

import random

from .integration_constants import (
    BASE_NORMALIZATION_TURNS,
    NORMALIZATION_TRAIT_MODIFIERS,
    MAX_NORMALIZATION_STABILITY_PENALTY,
    MAX_NORMALIZATION_HAPPINESS_PENALTY,
    MISMATCH_STRONG_WEIGHT,
    MISMATCH_WEAK_WEIGHT,
    UNCLAIMED_DRIFT_RATE,
)


# ---------------------------------------------------------------------------
# Ideology mismatch
# ---------------------------------------------------------------------------

def compute_ideology_mismatch(province_traits: dict, nation_traits: dict) -> float:
    """
    Return a 0.0–1.0 score measuring how different province ideology is from
    the nation's.

    Fully aligned → 0.0.  Fully opposed (all 3 slots differ) → 1.0.

    Scoring:
      Strong trait slot:  +MISMATCH_STRONG_WEIGHT (1/3) if different
      Each weak trait:    +MISMATCH_WEAK_WEIGHT   (1/6) if not in the
                          other nation's weak set
    """
    if not province_traits or not nation_traits:
        return 0.0

    prov_strong = province_traits.get("strong")
    prov_weak   = set(province_traits.get("weak", []))
    nat_strong  = nation_traits.get("strong")
    nat_weak    = set(nation_traits.get("weak", []))

    mismatch = 0.0

    # Strong trait slot
    if prov_strong and nat_strong and prov_strong != nat_strong:
        mismatch += MISMATCH_STRONG_WEIGHT

    # Weak trait slots
    for w in prov_weak:
        if w not in nat_weak:
            mismatch += MISMATCH_WEAK_WEIGHT

    return min(1.0, mismatch)


# ---------------------------------------------------------------------------
# Normalization progress
# ---------------------------------------------------------------------------

def compute_normalization_progress(province, current_turn: int) -> float:
    """
    Return the normalization progress for a province as a float 0.0–1.0.

    1.0 means fully normalized (or is already a core province).
    0.0 means normalization just started.
    """
    if province.is_core or province.normalization_started_turn is None:
        return 1.0

    duration = province.normalization_duration or BASE_NORMALIZATION_TURNS
    elapsed = current_turn - province.normalization_started_turn
    return min(1.0, elapsed / max(1, duration))


# ---------------------------------------------------------------------------
# Normalization penalties
# ---------------------------------------------------------------------------

def compute_normalization_penalties(province, nation, current_turn: int):
    """
    Return (stability_penalty, happiness_penalty) for a non-core province.

    Both penalties decrease linearly from their maximum values (at progress=0)
    to zero (at progress=1). The magnitude also scales with ideology mismatch —
    a province that shares ideology with the nation has smaller penalties.

    Parameters
    ----------
    province : Province
    nation : Nation
    current_turn : int

    Returns
    -------
    (stability_penalty, happiness_penalty) : (float, float)
        Positive values — caller subtracts these from stability/happiness.
    """
    progress = compute_normalization_progress(province, current_turn)
    if progress >= 1.0:
        return 0.0, 0.0

    mismatch = compute_ideology_mismatch(
        province.ideology_traits or {},
        nation.ideology_traits or {},
    )

    remaining = 1.0 - progress
    stab_penalty = MAX_NORMALIZATION_STABILITY_PENALTY * mismatch * remaining
    hap_penalty  = MAX_NORMALIZATION_HAPPINESS_PENALTY * mismatch * remaining

    return stab_penalty, hap_penalty


# ---------------------------------------------------------------------------
# Normalization duration
# ---------------------------------------------------------------------------

def get_normalization_duration(nation, control: float = 100.0) -> int:
    """
    Compute the normalization duration (in turns) for a nation based on its
    ideology traits and the province's control level.

    Base: BASE_NORMALIZATION_TURNS (120 = 10 years).
    Internationalist reduces the duration; Nationalist increases it.
    Lower control slows normalization (via compute_normalization_control_multiplier).
    """
    duration = BASE_NORMALIZATION_TURNS
    traits = nation.ideology_traits or {}
    strong = traits.get("strong")
    weak_list = traits.get("weak", [])

    all_traits = [strong] + list(weak_list)
    for trait in all_traits:
        if trait is None:
            continue
        strength = "strong" if trait == strong else "weak"
        modifier = NORMALIZATION_TRAIT_MODIFIERS.get(trait, {}).get(strength, 0)
        duration += modifier

    from .control import compute_normalization_control_multiplier
    duration = int(duration * compute_normalization_control_multiplier(control))

    return max(12, duration)  # minimum 1 year


# ---------------------------------------------------------------------------
# Starting normalization
# ---------------------------------------------------------------------------

def start_normalization(province, nation, current_turn: int) -> None:
    """
    Begin the normalization process for a province newly acquired by a nation.

    Sets:
      - province.nation          = nation
      - province.is_core         = False
      - province.normalization_started_turn = current_turn
      - province.normalization_duration     = get_normalization_duration(nation)
      - province.original_nation (if not already set)

    Province ideology_traits are NOT changed here — they should already be set
    to the province's own ideology before calling this (e.g. from the old
    nation, or randomly assigned for unclaimed provinces).
    """
    from .control import get_province_control
    # Wealth & Taxation: estate tax applies at point of acquisition, before reassignment.
    try:
        from .pricing import compute_turn_start_prices
        from .taxation import collect_estate_tax
        prices = compute_turn_start_prices(nation)["prices"]
        collect_estate_tax(nation, province, prices)
    except Exception:
        pass

    province.nation = nation
    province.is_core = False
    province.normalization_started_turn = current_turn
    province.normalization_duration = get_normalization_duration(nation, control=get_province_control(province))

    if province.original_nation_id is None:
        province.original_nation = nation


def check_normalization_completion(province, nation, current_turn: int) -> bool:
    """
    Check if a non-core province has finished normalizing. If so, align its
    ideology to the national ideology and mark it as core.

    Returns True if normalization just completed, False otherwise.
    """
    if province.is_core:
        return False

    progress = compute_normalization_progress(province, current_turn)
    if progress < 1.0:
        return False

    # Normalization complete — align ideology and promote to core.
    province.ideology_traits = nation.ideology_traits or {}
    province.is_core = True
    province.normalization_started_turn = None
    province.normalization_duration = None
    return True


# ---------------------------------------------------------------------------
# Location requirements for province acquisition
# ---------------------------------------------------------------------------

def check_location_requirements(province, nation) -> bool:
    """
    Validate that a target province is geographically eligible for acquisition
    by the given nation. At least one of the following must be true:

    1. The province borders ≥ 2 provinces owned by the nation.
    2. The province borders ≥ 1 national province AND shares an adjacent
       sea_zone or river_zone with any national province.
    3. The province is adjacent to a sea_zone AND the shortest path from
       the target to any national port-province via sea zones is ≤ the
       number of naval_base buildings the nation has.

    Parameters
    ----------
    province : Province
        The unclaimed target province.
    nation : Nation
        The acquiring nation.

    Returns
    -------
    bool
    """
    from provinces.models import Building

    # --- Condition 1 & 2: land/coastal adjacency ---
    nat_province_ids = set(
        nation.provinces.values_list("id", flat=True)
    )
    adjacent_national = province.adjacent_provinces.filter(
        nation=nation
    )
    adjacent_national_count = adjacent_national.count()

    if adjacent_national_count >= 2:
        return True

    if adjacent_national_count >= 1:
        # Check sea/river zone overlap with any national province
        province_sea_ids  = set(province.adjacent_sea_zones.values_list("id", flat=True))
        province_river_ids = set(province.adjacent_river_zones.values_list("id", flat=True))

        if province_sea_ids or province_river_ids:
            from provinces.models import Province as Prov
            national_provinces = Prov.objects.filter(nation=nation).prefetch_related(
                "adjacent_sea_zones", "adjacent_river_zones"
            )
            for np in national_provinces:
                np_sea   = set(np.adjacent_sea_zones.values_list("id", flat=True))
                np_river = set(np.adjacent_river_zones.values_list("id", flat=True))
                if province_sea_ids & np_sea or province_river_ids & np_river:
                    return True

    # --- Condition 3: naval reach ---
    # Target must be adjacent to a sea zone.
    target_sea_ids = set(province.adjacent_sea_zones.values_list("id", flat=True))
    if not target_sea_ids:
        return False

    naval_base_count = Building.objects.filter(
        province__nation=nation,
        building_type="naval_base",
        is_active=True,
        under_construction=False,
    ).count()

    if naval_base_count == 0:
        return False

    # Find national provinces with a port building adjacent to a sea zone.
    port_provinces = Building.objects.filter(
        province__nation=nation,
        building_type__in=("port", "dock"),
        is_active=True,
        under_construction=False,
    ).values_list("province_id", flat=True)

    if not port_provinces:
        return False

    # BFS from target sea zones to any sea zone adjacent to a port province.
    from provinces.models import SeaZone, Province as Prov

    # Build target reachable sea zones within naval_base_count hops.
    visited = set(target_sea_ids)
    frontier = set(target_sea_ids)
    for _ in range(naval_base_count):
        next_frontier = set()
        for sz_id in frontier:
            try:
                sz = SeaZone.objects.prefetch_related("adjacent_sea_zones").get(pk=sz_id)
                for adj in sz.adjacent_sea_zones.all():
                    if adj.id not in visited:
                        visited.add(adj.id)
                        next_frontier.add(adj.id)
            except SeaZone.DoesNotExist:
                pass
        frontier = next_frontier
        if not frontier:
            break

    # Check if any port province's sea zones are in the reachable set.
    port_sea_ids = set(
        Prov.objects.filter(
            id__in=port_provinces
        ).values_list("adjacent_sea_zones", flat=True)
    )
    port_sea_ids.discard(None)

    return bool(visited & port_sea_ids)


# ---------------------------------------------------------------------------
# Unclaimed province ideology drift
# ---------------------------------------------------------------------------

def drift_unclaimed_ideology(province) -> None:
    """
    Randomly drift the ideology traits of an unclaimed province each turn.

    At UNCLAIMED_DRIFT_RATE probability, one trait slot shifts to a random
    valid trait from a different pair. This simulates natural ideological
    fragmentation in ungoverned territory.

    Only fires probabilistically — call every turn for unclaimed provinces.
    """
    from nations.trait_constants import TRAIT_PAIRS, TRAIT_DEFS

    if random.random() > UNCLAIMED_DRIFT_RATE:
        return  # no drift this turn

    current_traits = province.ideology_traits or {}
    strong = current_traits.get("strong")
    weak_list = list(current_traits.get("weak", []))

    if not strong and not weak_list:
        # Province has no ideology — assign a random valid one.
        pairs = list(TRAIT_PAIRS)
        random.shuffle(pairs)
        strong = random.choice(pairs[0])
        weak_list = [random.choice(p) for p in pairs[1:3]]
        province.ideology_traits = {"strong": strong, "weak": weak_list}
        return

    # Pick a random slot to drift (0=strong, 1=weak[0], 2=weak[1])
    slot = random.randint(0, 2)

    if slot == 0 and strong:
        # Pick a random trait from a different pair than current strong.
        current_pair_idx = TRAIT_DEFS.get(strong, {}).get("pair_index", -1)
        candidates = [
            t for t in TRAIT_DEFS
            if TRAIT_DEFS[t].get("pair_index") != current_pair_idx
        ]
        if candidates:
            province.ideology_traits = {
                "strong": random.choice(candidates),
                "weak": weak_list,
            }
    elif 1 <= slot <= 2 and len(weak_list) > slot - 1:
        idx = slot - 1
        current_weak = weak_list[idx]
        current_pair_idx = TRAIT_DEFS.get(current_weak, {}).get("pair_index", -1)
        # Must not use same pair as strong or other weak
        used_pairs = {
            TRAIT_DEFS.get(strong, {}).get("pair_index", -1),
            TRAIT_DEFS.get(weak_list[1 - idx] if len(weak_list) > 1 - idx else None, {}).get("pair_index", -1),
            current_pair_idx,
        }
        candidates = [
            t for t in TRAIT_DEFS
            if TRAIT_DEFS[t].get("pair_index") not in used_pairs
        ]
        if candidates:
            new_weak = list(weak_list)
            new_weak[idx] = random.choice(candidates)
            province.ideology_traits = {"strong": strong, "weak": new_weak}
