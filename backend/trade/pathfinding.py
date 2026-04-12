"""
Trade route pathfinder — Dijkstra over the province/zone adjacency graph.

The graph has four node types:
  ("prov",  province_id)
  ("sea",   sea_zone_id)
  ("river", river_zone_id)
  ("air",   air_zone_id)

Edge weights are effective distances (map-unit equivalents) so every domain
uses a single comparable cost unit.

Domain tagging:
  prov↔prov  = "land"
  prov↔sea   = "sea"  (requires port or dock at province)
  prov↔river = "land" (rivers bill to the land capacity pool)
  prov↔air   = "air"  (requires air_cargo_terminal at province)
  sea↔sea    = "sea"
  river↔river= "land"
  air↔air    = "air"
  sea↔river  = "sea"  (river mouth → sea)
  river↔sea  = "sea"

No sea↔air edges (per spec).

Usage:
  graph = build_trade_graph(game_id, allowed_domains=None)
  result = find_shortest_path(graph, source_node, dest_node)

  result = PathResult(
      path=[node, ...],
      total_length=float,
      domain_segments={"land": float, "sea": float, "air": float},
  )
"""
from __future__ import annotations

import heapq
from dataclasses import dataclass, field

from .constants import EMBARK_DISTANCE, ZONE_HOP_DISTANCE
from .distance import effective_land_distance_simple


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

Node = tuple[str, int]  # ("prov", id) | ("sea", id) | ("river", id) | ("air", id)


@dataclass
class Edge:
    to: Node
    weight: float
    domain: str  # "land", "sea", or "air"


@dataclass
class TradeGraph:
    """Adjacency-list graph for trade pathfinding."""
    adjacency: dict[Node, list[Edge]] = field(default_factory=dict)

    def add_edge(self, a: Node, b: Node, weight: float, domain: str):
        self.adjacency.setdefault(a, []).append(Edge(b, weight, domain))
        self.adjacency.setdefault(b, []).append(Edge(a, weight, domain))


@dataclass
class PathResult:
    path: list[Node]
    total_length: float
    domain_segments: dict[str, float]  # {"land": X, "sea": Y, "air": Z}


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------

def build_trade_graph(
    game_id: int,
    allowed_domains: set[str] | None = None,
) -> TradeGraph:
    """Build the trade pathfinding graph for a game.

    Parameters
    ----------
    game_id : int
    allowed_domains : optional set of {"land", "sea", "air"}.
        If provided, only edges in these domains are included.
        None means all domains.

    Returns
    -------
    TradeGraph with all nodes and edges for the game's geography.
    """
    from provinces.models import Province, SeaZone, RiverZone, AirZone, Building

    graph = TradeGraph()
    allow_land = allowed_domains is None or "land" in allowed_domains
    allow_sea = allowed_domains is None or "sea" in allowed_domains
    allow_air = allowed_domains is None or "air" in allowed_domains

    # -- Prefetch provinces and their data --
    provinces = list(
        Province.objects.filter(game_id=game_id)
        .select_related("air_zone")
        .prefetch_related(
            "adjacent_provinces",
            "adjacent_sea_zones",
            "adjacent_river_zones",
        )
    )
    prov_by_id = {p.pk: p for p in provinces}

    # Prefetch which building types are active in each province
    active_buildings = {}
    for b in Building.objects.filter(
        province__game_id=game_id,
        is_active=True,
        under_construction=False,
    ).values_list("province_id", "building_type"):
        active_buildings.setdefault(b[0], set()).add(b[1])

    # Helper: does a province have a building that satisfies a trade transition?
    def _has_port(prov_id):
        bldgs = active_buildings.get(prov_id, set())
        return bool(bldgs & {"port", "dock"})

    def _has_air_cargo(prov_id):
        bldgs = active_buildings.get(prov_id, set())
        return "air_cargo_terminal" in bldgs

    # -- Province ↔ Province (land) --
    if allow_land:
        seen_pairs = set()
        for p in provinces:
            for adj in p.adjacent_provinces.all():
                pair = (min(p.pk, adj.pk), max(p.pk, adj.pk))
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)
                adj_prov = prov_by_id.get(adj.pk)
                if adj_prov is None:
                    continue
                w = effective_land_distance_simple(p, adj_prov)
                graph.add_edge(("prov", p.pk), ("prov", adj.pk), w, "land")

    # -- Province ↔ Sea zone (sea domain, requires port/dock) --
    if allow_sea:
        for p in provinces:
            if not _has_port(p.pk):
                continue
            for sz in p.adjacent_sea_zones.all():
                w = EMBARK_DISTANCE["sea"]
                graph.add_edge(("prov", p.pk), ("sea", sz.pk), w, "sea")

    # -- Province ↔ River zone (land domain, no building requirement) --
    if allow_land:
        for p in provinces:
            for rz in p.adjacent_river_zones.all():
                w = EMBARK_DISTANCE["river"]
                graph.add_edge(("prov", p.pk), ("river", rz.pk), w, "land")

    # -- Province ↔ Air zone (air domain, requires air_cargo_terminal) --
    if allow_air:
        for p in provinces:
            if not _has_air_cargo(p.pk):
                continue
            if p.air_zone_id is not None:
                w = EMBARK_DISTANCE["air"]
                graph.add_edge(("prov", p.pk), ("air", p.air_zone_id), w, "air")

    # -- Sea zone ↔ Sea zone --
    if allow_sea:
        sea_zones = list(
            SeaZone.objects.filter(game_id=game_id)
            .prefetch_related("adjacent_sea_zones")
        )
        seen = set()
        for sz in sea_zones:
            for adj in sz.adjacent_sea_zones.all():
                pair = (min(sz.pk, adj.pk), max(sz.pk, adj.pk))
                if pair in seen:
                    continue
                seen.add(pair)
                graph.add_edge(("sea", sz.pk), ("sea", adj.pk), ZONE_HOP_DISTANCE["sea"], "sea")

    # -- River zone ↔ River zone (land domain) --
    if allow_land:
        river_zones = list(
            RiverZone.objects.filter(game_id=game_id)
            .prefetch_related("adjacent_river_zones")
        )
        seen = set()
        for rz in river_zones:
            for adj in rz.adjacent_river_zones.all():
                pair = (min(rz.pk, adj.pk), max(rz.pk, adj.pk))
                if pair in seen:
                    continue
                seen.add(pair)
                graph.add_edge(("river", rz.pk), ("river", adj.pk), ZONE_HOP_DISTANCE["river"], "land")

    # -- River zone ↔ Sea zone (river mouth, sea domain) --
    if allow_sea:
        for rz in RiverZone.objects.filter(game_id=game_id, sea_zone__isnull=False):
            graph.add_edge(
                ("river", rz.pk),
                ("sea", rz.sea_zone_id),
                EMBARK_DISTANCE["sea"],
                "sea",
            )

    # -- Air zone ↔ Air zone --
    if allow_air:
        air_zones = list(
            AirZone.objects.filter(game_id=game_id)
            .prefetch_related("adjacent_air_zones")
        )
        seen = set()
        for az in air_zones:
            for adj in az.adjacent_air_zones.all():
                pair = (min(az.pk, adj.pk), max(az.pk, adj.pk))
                if pair in seen:
                    continue
                seen.add(pair)
                graph.add_edge(("air", az.pk), ("air", adj.pk), ZONE_HOP_DISTANCE["air"], "air")

    # No sea↔air edges (per spec).

    return graph


# ---------------------------------------------------------------------------
# Dijkstra
# ---------------------------------------------------------------------------

def find_shortest_path(
    graph: TradeGraph,
    source: Node,
    dest: Node,
) -> PathResult | None:
    """Find the shortest (minimum total weight) path between two nodes.

    Returns PathResult on success, None if no path exists.
    """
    dist: dict[Node, float] = {source: 0.0}
    prev: dict[Node, tuple[Node, Edge] | None] = {source: None}
    visited: set[Node] = set()
    # heap entries: (distance, node)
    heap: list[tuple[float, Node]] = [(0.0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)

        if u == dest:
            break

        for edge in graph.adjacency.get(u, []):
            v = edge.to
            if v in visited:
                continue
            nd = d + edge.weight
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = (u, edge)
                heapq.heappush(heap, (nd, v))

    if dest not in prev:
        return None

    # Reconstruct path and domain segments
    path: list[Node] = []
    domain_segments: dict[str, float] = {"land": 0.0, "sea": 0.0, "air": 0.0}
    node = dest
    while node is not None:
        path.append(node)
        entry = prev.get(node)
        if entry is not None:
            parent, edge = entry
            domain_segments[edge.domain] = domain_segments.get(edge.domain, 0.0) + edge.weight
            node = parent
        else:
            node = None

    path.reverse()

    return PathResult(
        path=path,
        total_length=dist[dest],
        domain_segments=domain_segments,
    )


def find_trade_route_path(
    game_id: int,
    from_province_id: int,
    to_province_id: int,
    domain_mode: str = "multi",
) -> PathResult | None:
    """High-level helper: find the shortest trade path between two provinces.

    Parameters
    ----------
    game_id : int
    from_province_id, to_province_id : int — province PKs (typically capitals).
    domain_mode : "multi" | "land" | "sea" | "air"
        "multi" allows all domains. Others restrict to a single domain
        (plus land, since "sea" and "air" still need land legs to reach ports).

    Returns
    -------
    PathResult or None if no path exists.
    """
    if domain_mode == "multi":
        allowed = None
    elif domain_mode == "land":
        allowed = {"land"}
    elif domain_mode == "sea":
        allowed = {"land", "sea"}  # need land legs to reach ports
    elif domain_mode == "air":
        allowed = {"land", "air"}  # need land legs to reach air cargo terminals
    else:
        allowed = None

    graph = build_trade_graph(game_id, allowed_domains=allowed)
    return find_shortest_path(
        graph,
        ("prov", from_province_id),
        ("prov", to_province_id),
    )
