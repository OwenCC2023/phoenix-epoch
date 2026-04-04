from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from games.models import Game
from nations.models import Nation

from .construction import get_nation_under_construction
from .models import NationGoodStock, NationResourcePool, ResearchUnlock, ResourceLedger, TradeOffer
from .serializers import (
    ConstructionBuildingSerializer,
    NationGoodStockSerializer,
    NationResourcePoolSerializer,
    ResourceLedgerSerializer,
    TradeOfferSerializer,
    TradeOfferCreateSerializer,
)


class NationConstructionView(APIView):
    """
    GET /api/games/{game_id}/nations/{nation_id}/construction/

    Returns all items currently under construction for a nation, grouped by
    type.  New constructible types (military units, etc.) appear automatically
    once get_nation_under_construction() is updated to include them.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id, nation_id):
        try:
            nation = Nation.objects.get(pk=nation_id, game_id=game_id)
        except Nation.DoesNotExist:
            return Response({"detail": "Nation not found."}, status=status.HTTP_404_NOT_FOUND)

        items = get_nation_under_construction(nation)

        return Response({
            "buildings": ConstructionBuildingSerializer(items["buildings"], many=True).data,
            # Future types will appear here automatically.
        })


class NationGoodStockView(generics.RetrieveAPIView):
    """GET /api/games/{game_id}/nations/{nation_id}/goods/"""

    serializer_class = NationGoodStockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        good_stock, _ = NationGoodStock.objects.get_or_create(
            nation_id=self.kwargs["nation_id"],
        )
        return good_stock


class NationResourcePoolView(generics.RetrieveAPIView):
    """GET /api/games/{game_id}/nations/{nation_id}/resources/"""

    serializer_class = NationResourcePoolSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        pool, _ = NationResourcePool.objects.get_or_create(
            nation_id=self.kwargs["nation_id"],
        )
        return pool


class ResourceLedgerListView(generics.ListAPIView):
    """GET /api/games/{game_id}/nations/{nation_id}/ledger/"""

    serializer_class = ResourceLedgerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResourceLedger.objects.filter(
            nation_id=self.kwargs["nation_id"],
            nation__game_id=self.kwargs["game_id"],
        )


class TradeOfferListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/games/{game_id}/trades/   - List trades in a game
    POST /api/games/{game_id}/trades/   - Create a new trade offer
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TradeOffer.objects.filter(
            game_id=self.kwargs["game_id"],
        ).select_related("from_nation", "to_nation")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TradeOfferCreateSerializer
        return TradeOfferSerializer

    def create(self, request, *args, **kwargs):
        game_id = self.kwargs["game_id"]

        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return Response(
                {"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Sender must have a nation in this game
        try:
            from_nation = Nation.objects.get(game=game, player=request.user, is_alive=True)
        except Nation.DoesNotExist:
            return Response(
                {"detail": "You do not have a living nation in this game."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        to_nation_id = serializer.validated_data["to_nation"]

        # Cannot trade with yourself
        if to_nation_id == from_nation.id:
            return Response(
                {"detail": "You cannot trade with yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Target nation must be in the same game and alive
        try:
            to_nation = Nation.objects.get(pk=to_nation_id, game=game, is_alive=True)
        except Nation.DoesNotExist:
            return Response(
                {"detail": "Target nation not found or not alive in this game."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        trade = TradeOffer.objects.create(
            game=game,
            from_nation=from_nation,
            to_nation=to_nation,
            turn_number=game.current_turn_number,
            offering=serializer.validated_data["offering"],
            requesting=serializer.validated_data["requesting"],
        )

        return Response(
            TradeOfferSerializer(trade, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
        )


class NationResearchView(APIView):
    """
    GET /api/games/{game_id}/nations/{nation_id}/research/

    Returns:
      - current research pool amount
      - national literacy (from pool)
      - list of unlocked sectors with their current tier
      - list of available next unlocks with costs
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id, nation_id):
        from .research_constants import RESEARCH_UNLOCK_COSTS

        try:
            nation = Nation.objects.get(pk=nation_id, game_id=game_id)
        except Nation.DoesNotExist:
            return Response({"detail": "Nation not found."}, status=status.HTTP_404_NOT_FOUND)

        pool, _ = NationResourcePool.objects.get_or_create(nation=nation)
        unlocks = {u.sector: u.tier for u in ResearchUnlock.objects.filter(nation=nation)}

        available_unlocks = []
        for sector, tier_costs in RESEARCH_UNLOCK_COSTS.items():
            current_tier = unlocks.get(sector, 0)
            next_tier = current_tier + 1
            if next_tier in tier_costs:
                available_unlocks.append({
                    "sector": sector,
                    "current_tier": current_tier,
                    "next_tier": next_tier,
                    "cost": tier_costs[next_tier],
                    "can_afford": pool.research >= tier_costs[next_tier],
                })

        return Response({
            "research": pool.research,
            "national_literacy": pool.literacy,
            "unlocked_sectors": [
                {"sector": s, "tier": t} for s, t in sorted(unlocks.items())
            ],
            "available_unlocks": available_unlocks,
        })


class NationAcquirableProvincesView(APIView):
    """
    GET /api/games/{game_id}/nations/{nation_id}/acquirable/

    Returns unclaimed provinces in this game that pass location requirements
    for the given nation, along with the economic acquisition cost.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id, nation_id):
        from provinces.models import Province
        from economy.normalization import check_location_requirements
        from economy.integration_constants import ECONOMIC_ACQUISITION_COSTS

        try:
            nation = Nation.objects.get(pk=nation_id, game_id=game_id)
        except Nation.DoesNotExist:
            return Response({"detail": "Nation not found."}, status=status.HTTP_404_NOT_FOUND)

        unclaimed = Province.objects.filter(
            game_id=game_id,
            nation__isnull=True,
        ).prefetch_related("adjacent_provinces", "adjacent_sea_zones", "adjacent_river_zones")

        acquirable = []
        for province in unclaimed:
            if check_location_requirements(province, nation):
                acquirable.append({
                    "province_id": province.id,
                    "name": province.name,
                    "terrain_type": province.terrain_type,
                    "population": province.population,
                    "ideology_traits": province.ideology_traits,
                    "acquisition_cost": ECONOMIC_ACQUISITION_COSTS,
                })

        return Response({"acquirable_provinces": acquirable})


class TradeOfferResponseView(APIView):
    """POST /api/games/{game_id}/trades/{pk}/respond/ with {"action": "accept"/"reject"}"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, game_id, pk):
        try:
            trade = TradeOffer.objects.select_related("to_nation", "from_nation").get(
                pk=pk, game_id=game_id
            )
        except TradeOffer.DoesNotExist:
            return Response(
                {"detail": "Trade offer not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Only the recipient can respond
        if trade.to_nation.player != request.user:
            return Response(
                {"detail": "Only the recipient nation's player can respond to this trade."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if trade.status != TradeOffer.Status.PENDING:
            return Response(
                {"detail": f"Trade is already {trade.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        action = request.data.get("action")
        if action not in ("accept", "reject"):
            return Response(
                {"detail": "Action must be 'accept' or 'reject'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if action == "reject":
            trade.status = TradeOffer.Status.REJECTED
            trade.save(update_fields=["status"])
            return Response(TradeOfferSerializer(trade).data)

        # Accept — mark as accepted (actual resource transfer happens during turn resolution)
        trade.status = TradeOffer.Status.ACCEPTED
        trade.save(update_fields=["status"])
        return Response(TradeOfferSerializer(trade).data)
