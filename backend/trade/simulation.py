"""
Trade simulation helpers called from economy/simulation.py each turn.

Two phases per turn:

  process_trade_imports(nation, turn_number, pool, good_stock)
      Import phase (Step 8): deliver any in-flight shipments whose
      arrives_turn <= current turn. Adds to pool/good_stock and writes
      the positive side of trade_net.

  process_trade_exports(nation, turn_number, pool, good_stock)
      Export phase (Step 16.5): for each active route, deduct quantity
      from exporter (capped at available), push to in_flight, write
      the negative side of trade_net.

Between these two calls the main simulation uses pool/good_stock normally
(upkeep, consumption, military deductions), so imports are available for
the current-turn economy and exports use post-spend leftovers.

Returns a dict compatible with the ResourceLedger's trade_net field:
  {"food": float, "materials": float, ...}  (positive = net import)

Goods split:
  Pool resources  (food, materials, energy, wealth, manpower, research)
      → NationResourcePool fields
  Manufactured    (consumer_goods, arms, fuel, machinery, chemicals,
                   medicine, components, heavy_equipment, military_goods)
      → NationGoodStock fields
"""
from __future__ import annotations

_POOL_FIELDS = frozenset(["food", "materials", "energy", "wealth", "manpower", "research"])
_GOOD_FIELDS = frozenset([
    "consumer_goods", "arms", "fuel", "machinery", "chemicals",
    "medicine", "components", "heavy_equipment", "military_goods",
])


def _add_good(good: str, amount: float, pool, good_stock):
    """Add amount of good to the correct storage model."""
    if good in _POOL_FIELDS:
        setattr(pool, good, round(getattr(pool, good, 0.0) + amount, 4))
    elif good in _GOOD_FIELDS:
        setattr(good_stock, good, round(getattr(good_stock, good, 0.0) + amount, 4))


def _deduct_good(good: str, amount: float, pool, good_stock) -> float:
    """Deduct up to amount of good from storage. Returns actual amount deducted."""
    if good in _POOL_FIELDS:
        available = max(0.0, getattr(pool, good, 0.0))
        actual = min(amount, available)
        setattr(pool, good, round(available - actual, 4))
        return actual
    elif good in _GOOD_FIELDS:
        available = max(0.0, getattr(good_stock, good, 0.0))
        actual = min(amount, available)
        setattr(good_stock, good, round(available - actual, 4))
        return actual
    return 0.0


def _save_pool_stock(pool, good_stock):
    pool.save()
    good_stock.save()


def process_trade_imports(nation, turn_number: int, pool, good_stock) -> dict:
    """Deliver in-flight goods that have arrived. Returns net import dict."""
    from .models import TradeRoute

    trade_net: dict[str, float] = {}

    active_routes = list(
        TradeRoute.objects.filter(to_nation=nation, status=TradeRoute.Status.ACTIVE)
    )
    if not active_routes:
        return trade_net

    pool_dirty = False
    stock_dirty = False

    for route in active_routes:
        in_flight = route.in_flight or []
        arrived = [s for s in in_flight if s["arrives_turn"] <= turn_number]
        still_flying = [s for s in in_flight if s["arrives_turn"] > turn_number]

        if not arrived:
            continue

        total_arrived = sum(s["quantity"] for s in arrived)
        _add_good(route.good, total_arrived, pool, good_stock)

        if route.good in _POOL_FIELDS:
            pool_dirty = True
        else:
            stock_dirty = True

        trade_net[route.good] = trade_net.get(route.good, 0.0) + total_arrived

        route.in_flight = still_flying
        route.save(update_fields=["in_flight"])

    if pool_dirty or stock_dirty:
        if pool_dirty:
            pool.save()
        if stock_dirty:
            good_stock.save()

    return trade_net


def process_trade_exports(nation, turn_number: int, pool, good_stock) -> dict:
    """Deduct exports from nation's stocks and push to in_flight. Returns net export dict (negative values)."""
    from .models import TradeRoute
    from .pathfinding import find_trade_route_path

    trade_net: dict[str, float] = {}

    outgoing = list(
        TradeRoute.objects.filter(
            from_nation=nation,
            status__in=[TradeRoute.Status.ACTIVE, TradeRoute.Status.PENDING],
        )
    )
    if not outgoing:
        return trade_net

    pool_dirty = False
    stock_dirty = False

    for route in outgoing:
        # Verify path still exists (capitals may have moved)
        from_cap = nation.get_effective_capital()
        to_cap = route.to_nation.get_effective_capital()

        if from_cap is None or to_cap is None:
            route.status = TradeRoute.Status.INACTIVE_WAR
            route.save(update_fields=["status"])
            continue

        # Deduct from exporter (cap at what's actually available)
        actual = _deduct_good(route.good, route.quantity_per_turn, pool, good_stock)
        if actual == 0:
            # Nothing to export this turn — skip but keep route active
            continue

        if route.good in _POOL_FIELDS:
            pool_dirty = True
        else:
            stock_dirty = True

        # Push to in_flight
        in_flight = list(route.in_flight or [])
        in_flight.append({
            "quantity": actual,
            "arrives_turn": turn_number + route.arrival_turns,
        })
        route.in_flight = in_flight
        if route.status == TradeRoute.Status.PENDING:
            route.status = TradeRoute.Status.ACTIVE
        route.save(update_fields=["in_flight", "status"])

        trade_net[route.good] = trade_net.get(route.good, 0.0) - actual

    if pool_dirty:
        pool.save()
    if stock_dirty:
        good_stock.save()

    return trade_net


def recompute_route_paths(game, turn_number: int):
    """Recompute paths for all ACTIVE/PENDING routes in a game each turn.

    Called once per turn (before exports) to catch changes to adjacency or capitals.
    Routes with no valid path are set to BROKEN_PATH.
    Routes with a lost capital are set to INACTIVE_WAR.
    """
    from .models import TradeRoute
    from .pathfinding import find_trade_route_path
    from trade.constants import TRADE_SPEED_PER_TURN, MIN_ARRIVAL_TURNS
    import math

    routes = list(
        TradeRoute.objects.filter(
            game=game,
            status__in=[TradeRoute.Status.ACTIVE, TradeRoute.Status.PENDING],
        ).select_related("from_nation", "to_nation")
    )

    for route in routes:
        from_cap = route.from_nation.get_effective_capital()
        to_cap = route.to_nation.get_effective_capital()

        if from_cap is None or to_cap is None:
            route.status = TradeRoute.Status.INACTIVE_WAR
            route.save(update_fields=["status"])
            continue

        result = find_trade_route_path(
            game.pk, from_cap.pk, to_cap.pk, route.domain_mode
        )

        if result is None:
            route.status = TradeRoute.Status.BROKEN_PATH
            route.save(update_fields=["status"])
            continue

        arrival_turns = max(MIN_ARRIVAL_TURNS, math.ceil(result.total_length / TRADE_SPEED_PER_TURN))

        route.path_nodes = [[n[0], n[1]] for n in result.path]
        route.total_length = result.total_length
        route.capacity_by_domain = result.domain_segments
        route.arrival_turns = arrival_turns
        route.save(update_fields=["path_nodes", "total_length", "capacity_by_domain", "arrival_turns"])
