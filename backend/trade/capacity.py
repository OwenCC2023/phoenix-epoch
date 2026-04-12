"""
Trade capacity helpers.

Each nation has three capacity pools: land, sea, air.

  pool[domain] = building_effects[f"{domain}_trade_capacity"]
                 × (1 + policy_trade_pct)         ← accumulated from policy_effects["trade_pct"]
                 × (1 + trait_capacity_bonus)      ← trade_capacity_bonus + trade_capacity_penalty

Route consumption:
  For each domain d that the route uses:
    consumed[d] += (capacity_by_domain[d] / CAPACITY_DISTANCE_NORMALISER) × quantity_per_turn

The validator checks whether adding a new route would exceed remaining capacity
in any domain it touches.
"""

from .constants import CAPACITY_DISTANCE_NORMALISER, DOMAIN_CAPACITY_EFFECT_KEY


# ---------------------------------------------------------------------------
# Pool computation
# ---------------------------------------------------------------------------

def get_trade_capacity(nation, provinces, nation_effects: dict, policy_effects: dict, trait_effects: dict) -> dict:
    """Compute available trade capacity pools for a nation.

    Parameters
    ----------
    nation : Nation instance (unused directly but kept for future trait hooks)
    provinces : iterable of Province instances for building effects
    nation_effects : dict from get_national_building_effects(provinces)
    policy_effects : dict from get_nation_policy_effects(nation)
    trait_effects  : dict from get_nation_trait_effects(nation)

    Returns
    -------
    dict with keys "land", "sea", "air" — float capacity units each.
    """
    # "trade_pct" is the key accumulated by get_nation_policy_effects()
    # from the trade_pct base effects in policy_effects_data.py.
    policy_pct = policy_effects.get("trade_pct", 0.0)

    # Trait bonuses/penalties on trade capacity (from trait_constants.py)
    trait_bonus = (
        trait_effects.get("trade_capacity_bonus", 0.0)
        + trait_effects.get("trade_capacity_penalty", 0.0)  # already negative
    )

    capacity = {}
    for domain, effect_key in DOMAIN_CAPACITY_EFFECT_KEY.items():
        base = nation_effects.get(effect_key, 0.0)
        capacity[domain] = max(0.0, base * (1.0 + policy_pct) * (1.0 + trait_bonus))

    return capacity


# ---------------------------------------------------------------------------
# Route capacity consumption
# ---------------------------------------------------------------------------

def route_capacity_consumption(capacity_by_domain: dict, quantity_per_turn: int) -> dict:
    """Compute capacity consumed per domain by a single trade route.

    Parameters
    ----------
    capacity_by_domain : {"land": float, "sea": float, "air": float}
        Domain-specific distances from the pathfinder result.
    quantity_per_turn : int — goods sent each turn.

    Returns
    -------
    dict with same keys, values are capacity units consumed.
    """
    consumed = {}
    for domain, dist in capacity_by_domain.items():
        consumed[domain] = (dist / CAPACITY_DISTANCE_NORMALISER) * quantity_per_turn
    return consumed


# ---------------------------------------------------------------------------
# Capacity used by existing routes
# ---------------------------------------------------------------------------

def get_used_capacity(nation) -> dict:
    """Sum capacity consumed by all active/pending trade routes for a nation.

    Returns dict {"land": float, "sea": float, "air": float}.
    """
    from .models import TradeRoute

    used = {"land": 0.0, "sea": 0.0, "air": 0.0}
    active_statuses = {TradeRoute.Status.ACTIVE, TradeRoute.Status.PENDING}
    for route in TradeRoute.objects.filter(
        from_nation=nation,
        status__in=active_statuses,
    ):
        consumed = route_capacity_consumption(route.capacity_by_domain, route.quantity_per_turn)
        for d in used:
            used[d] += consumed.get(d, 0.0)
    return used


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------

def validate_route_capacity(
    nation,
    provinces,
    nation_effects: dict,
    policy_effects: dict,
    trait_effects: dict,
    new_capacity_by_domain: dict,
    new_quantity: int,
    exclude_route_id: int | None = None,
) -> list[str]:
    """Check whether adding a route would exceed capacity in any domain.

    Parameters
    ----------
    nation, provinces, nation_effects, policy_effects, trait_effects :
        passed through to get_trade_capacity().
    new_capacity_by_domain : domain distances from pathfinder for the new route.
    new_quantity : goods per turn for the new route.
    exclude_route_id : optional PK of a route to exclude from used capacity
        (for editing an existing route).

    Returns
    -------
    list[str] — error messages (empty if valid).
    """
    from .models import TradeRoute

    available = get_trade_capacity(nation, provinces, nation_effects, policy_effects, trait_effects)
    used = {"land": 0.0, "sea": 0.0, "air": 0.0}

    active_statuses = {TradeRoute.Status.ACTIVE, TradeRoute.Status.PENDING}
    for route in TradeRoute.objects.filter(from_nation=nation, status__in=active_statuses):
        if exclude_route_id is not None and route.pk == exclude_route_id:
            continue
        consumed = route_capacity_consumption(route.capacity_by_domain, route.quantity_per_turn)
        for d in used:
            used[d] += consumed.get(d, 0.0)

    new_consumed = route_capacity_consumption(new_capacity_by_domain, new_quantity)

    errors = []
    for domain in ("land", "sea", "air"):
        avail = available.get(domain, 0.0)
        total = used.get(domain, 0.0) + new_consumed.get(domain, 0.0)
        if total > avail:
            errors.append(
                f"Insufficient {domain} trade capacity: need {total:.1f}, have {avail:.1f}."
            )
    return errors
