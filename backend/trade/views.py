"""Trade system API views."""
import math

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from games.models import Game
from nations.models import Nation

from .models import TradeRoute, CapitalRelocation
from .serializers import TradeRouteSerializer, CapitalRelocationSerializer, TradeRoutePreviewSerializer


def _get_game_and_nation(request, game_id):
    """Helper: fetch game and the requesting player's nation. Returns (game, nation, error_response)."""
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return None, None, Response({"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        nation = Nation.objects.get(game=game, player=request.user, is_alive=True)
    except Nation.DoesNotExist:
        return None, None, Response(
            {"detail": "You do not have a living nation in this game."},
            status=status.HTTP_403_FORBIDDEN,
        )

    return game, nation, None


class TradeRouteListView(generics.ListAPIView):
    """GET /api/games/<game_id>/trade/routes/ — list routes the nation is party to."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TradeRouteSerializer

    def get_queryset(self):
        game_id = self.kwargs["game_id"]
        game, nation, _ = _get_game_and_nation(self.request, game_id)
        if nation is None:
            return TradeRoute.objects.none()
        return TradeRoute.objects.filter(
            game_id=game_id,
        ).filter(
            from_nation=nation,
        ) | TradeRoute.objects.filter(
            game_id=game_id,
            to_nation=nation,
        )


class TradeRouteDetailView(generics.RetrieveAPIView):
    """GET /api/games/<game_id>/trade/routes/<pk>/ — detail for a single route."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TradeRouteSerializer

    def get_object(self):
        game_id = self.kwargs["game_id"]
        pk = self.kwargs["pk"]
        game, nation, _ = _get_game_and_nation(self.request, game_id)
        if nation is None:
            from django.http import Http404
            raise Http404
        try:
            route = TradeRoute.objects.get(pk=pk, game_id=game_id)
        except TradeRoute.DoesNotExist:
            from django.http import Http404
            raise Http404
        # Only parties to the route can view it
        if route.from_nation_id != nation.pk and route.to_nation_id != nation.pk:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not a party to this trade route.")
        return route


class TradeRoutePreviewView(APIView):
    """GET /api/games/<game_id>/trade/preview/

    Query params:
        to_nation_id: int
        good: str
        quantity_per_turn: int
        domain_mode: "multi" | "land" | "sea" | "air" (optional, default "multi")

    Returns pathfinder result + capacity check without creating anything.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id):
        game, nation, err = _get_game_and_nation(request, game_id)
        if err:
            return err

        to_nation_id = request.query_params.get("to_nation_id")
        good = request.query_params.get("good")
        quantity_str = request.query_params.get("quantity_per_turn", "1")
        domain_mode = request.query_params.get("domain_mode", "multi")

        if not to_nation_id or not good:
            return Response(
                {"detail": "to_nation_id and good are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return Response(
                {"detail": "quantity_per_turn must be a positive integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            to_nation = Nation.objects.get(pk=to_nation_id, game=game, is_alive=True)
        except Nation.DoesNotExist:
            return Response(
                {"detail": "Target nation not found."}, status=status.HTTP_404_NOT_FOUND
            )

        from_cap = nation.get_effective_capital()
        to_cap = to_nation.get_effective_capital()

        if from_cap is None or to_cap is None:
            return Response({
                "path_exists": False,
                "detail": "One or both nations have no active capital.",
            })

        from .pathfinding import find_trade_route_path
        from .capacity import get_trade_capacity, route_capacity_consumption, get_used_capacity
        from .constants import TRADE_SPEED_PER_TURN, MIN_ARRIVAL_TURNS
        from economy.building_simulation import get_national_building_effects
        from nations.helpers import get_nation_trait_effects
        from nations.policy_effects import get_nation_policy_effects

        result = find_trade_route_path(game.pk, from_cap.pk, to_cap.pk, domain_mode)

        if result is None:
            return Response({"path_exists": False})

        arrival_turns = max(MIN_ARRIVAL_TURNS, math.ceil(result.total_length / TRADE_SPEED_PER_TURN))

        provinces = list(nation.provinces.prefetch_related("buildings").all())
        nation_effects = get_national_building_effects(provinces)
        policy_effects = get_nation_policy_effects(nation)
        trait_effects = get_nation_trait_effects(nation)

        available = get_trade_capacity(nation, provinces, nation_effects, policy_effects, trait_effects)
        used = get_used_capacity(nation)
        consumed = route_capacity_consumption(result.domain_segments, quantity)

        data = {
            "path_exists": True,
            "path_nodes": [[n[0], n[1]] for n in result.path],
            "total_length": result.total_length,
            "domain_segments": result.domain_segments,
            "arrival_turns": arrival_turns,
            "capacity_consumed": consumed,
            "capacity_available": available,
            "capacity_used": used,
        }
        return Response(data)


class CapitalRelocationView(APIView):
    """GET /api/games/<game_id>/trade/capital-relocation/ — check pending relocation for your nation."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id):
        game, nation, err = _get_game_and_nation(request, game_id)
        if err:
            return err

        try:
            relocation = CapitalRelocation.objects.get(nation=nation)
            return Response(CapitalRelocationSerializer(relocation).data)
        except CapitalRelocation.DoesNotExist:
            return Response({"detail": "No capital relocation in progress."}, status=status.HTTP_404_NOT_FOUND)


class TradeCapacityView(APIView):
    """GET /api/games/<game_id>/trade/capacity/ — current capacity pools and usage for your nation."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id):
        game, nation, err = _get_game_and_nation(request, game_id)
        if err:
            return err

        from .capacity import get_trade_capacity, get_used_capacity
        from economy.building_simulation import get_national_building_effects
        from nations.helpers import get_nation_trait_effects
        from nations.policy_effects import get_nation_policy_effects

        provinces = list(nation.provinces.prefetch_related("buildings").all())
        nation_effects = get_national_building_effects(provinces)
        policy_effects = get_nation_policy_effects(nation)
        trait_effects = get_nation_trait_effects(nation)

        available = get_trade_capacity(nation, provinces, nation_effects, policy_effects, trait_effects)
        used = get_used_capacity(nation)
        remaining = {d: round(available[d] - used.get(d, 0.0), 2) for d in available}

        return Response({
            "available": available,
            "used": used,
            "remaining": remaining,
        })
