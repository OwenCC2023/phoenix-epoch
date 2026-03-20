from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AirZone, Building, Province, ProvinceSectorAllocation, RiverZone, SeaZone
from .serializers import (
    AirZoneSerializer,
    BuildingSerializer,
    ProvinceSectorAllocationBulkSerializer,
    ProvinceSectorAllocationSerializer,
    ProvinceSerializer,
    RiverZoneSerializer,
    SeaZoneSerializer,
)
from .building_constants import BUILDING_TYPES


class ProvinceListView(generics.ListAPIView):
    """
    GET /api/games/{game_id}/provinces/ - List all provinces in a game.

    Optional query param: ?nation_id= to filter by owning nation.
    """

    serializer_class = ProvinceSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Province.objects.filter(
            game_id=self.kwargs["game_id"]
        ).select_related("resources").prefetch_related("buildings")

        nation_id = self.request.query_params.get("nation_id")
        if nation_id is not None:
            qs = qs.filter(nation_id=nation_id)

        return qs


class ProvinceDetailView(generics.RetrieveAPIView):
    """
    GET /api/games/{game_id}/provinces/{pk}/ - Retrieve province details.
    """

    serializer_class = ProvinceSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Province.objects.filter(
            game_id=self.kwargs["game_id"]
        ).select_related("resources").prefetch_related("buildings")


class ProvinceAllocationView(APIView):
    """
    GET  /api/games/{game_id}/provinces/{pk}/allocations/ - Current allocations.
    POST /api/games/{game_id}/provinces/{pk}/allocations/ - Set allocations for next turn.
    """

    permission_classes = [permissions.IsAuthenticated]

    def _get_province(self, game_id, pk):
        try:
            return Province.objects.get(game_id=game_id, pk=pk)
        except Province.DoesNotExist:
            return None

    def get(self, request, game_id, pk):
        province = self._get_province(game_id, pk)
        if province is None:
            return Response(
                {"detail": "Province not found."}, status=status.HTTP_404_NOT_FOUND
            )

        allocations = province.sector_allocations.filter(
            turn_number=province.game.current_turn_number
        )
        serializer = ProvinceSectorAllocationSerializer(allocations, many=True)
        return Response(serializer.data)

    def post(self, request, game_id, pk):
        province = self._get_province(game_id, pk)
        if province is None:
            return Response(
                {"detail": "Province not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Validate user owns this province via nation
        if province.nation is None or province.nation.player != request.user:
            return Response(
                {"detail": "You do not own this province."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProvinceSectorAllocationBulkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        next_turn = province.game.current_turn_number + 1

        # Delete any existing allocations for next turn and recreate
        province.sector_allocations.filter(turn_number=next_turn).delete()

        allocations = []
        for item in serializer.validated_data["allocations"]:
            allocations.append(
                ProvinceSectorAllocation(
                    province=province,
                    sector=item["sector"],
                    percentage=item["percentage"],
                    turn_number=next_turn,
                )
            )
        ProvinceSectorAllocation.objects.bulk_create(allocations)

        result = ProvinceSectorAllocationSerializer(allocations, many=True)
        return Response(result.data, status=status.HTTP_201_CREATED)


class BuildingView(APIView):
    """
    GET  /api/games/{game_id}/provinces/{pk}/buildings/ - List buildings in province.
    POST /api/games/{game_id}/provinces/{pk}/buildings/ - Construct or upgrade a building.

    POST payload: {"building_type": "factory"}
    Builds level 1 if no building of that type exists, or upgrades existing building.
    Construction cost is immediately deducted from NationResourcePool.
    """

    permission_classes = [permissions.IsAuthenticated]

    def _get_province(self, game_id, pk):
        try:
            return Province.objects.select_related("game", "nation").get(game_id=game_id, pk=pk)
        except Province.DoesNotExist:
            return None

    def get(self, request, game_id, pk):
        province = self._get_province(game_id, pk)
        if province is None:
            return Response({"detail": "Province not found."}, status=status.HTTP_404_NOT_FOUND)

        buildings = province.buildings.all()
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)

    def post(self, request, game_id, pk):
        province = self._get_province(game_id, pk)
        if province is None:
            return Response({"detail": "Province not found."}, status=status.HTTP_404_NOT_FOUND)

        # Ownership check
        if province.nation is None or province.nation.player != request.user:
            return Response(
                {"detail": "You do not own this province."},
                status=status.HTTP_403_FORBIDDEN,
            )

        building_type = request.data.get("building_type")
        if not building_type:
            return Response(
                {"detail": "building_type is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        b_def = BUILDING_TYPES.get(building_type)
        if b_def is None:
            valid = ", ".join(sorted(BUILDING_TYPES.keys()))
            return Response(
                {"detail": f"Unknown building_type '{building_type}'. Valid: {valid}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Placement restrictions
        if building_type in ("dock", "port") and not province.is_coastal:
            return Response(
                {"detail": f"{b_def['label']}s can only be built in coastal provinces."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if building_type == "bridge" and not province.is_river:
            return Response(
                {"detail": "Bridges can only be built in river provinces."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if building_type == "naval_war_college" and not province.is_coastal:
            return Response(
                {"detail": "Naval War Colleges can only be built in coastal provinces."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Determine target level
        try:
            existing = province.buildings.get(building_type=building_type)
        except Building.DoesNotExist:
            existing = None

        # Nation-unique buildings: only one allowed across all provinces in the nation
        if b_def.get("unique_per_nation") and existing is None:
            nation_has_one = Building.objects.filter(
                province__nation=province.nation,
                building_type=building_type,
            ).exists()
            if nation_has_one:
                return Response(
                    {"detail": f"{b_def['label']} is a nation-unique building and your nation already has one."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if existing is not None:
            if existing.under_construction:
                return Response(
                    {"detail": "This building is already under construction."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if existing.level >= b_def["max_level"]:
                return Response(
                    {"detail": f"Building is already at max level ({b_def['max_level']})."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            target_level = existing.level + 1
        else:
            target_level = 1

        level_data = b_def["levels"][target_level - 1]
        cost = level_data["construction_cost"]

        # Deduct construction cost from NationResourcePool
        from economy.models import NationResourcePool

        pool, _ = NationResourcePool.objects.get_or_create(nation=province.nation)
        for resource, amount in cost.items():
            current = getattr(pool, resource, 0.0)
            if current < amount:
                return Response(
                    {"detail": f"Insufficient {resource}: need {amount}, have {current:.1f}."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        for resource, amount in cost.items():
            setattr(pool, resource, round(getattr(pool, resource) - amount, 4))
        pool.save(update_fields=list(cost.keys()))

        # Create or upgrade building
        turns = level_data["construction_turns"]
        if existing is not None:
            existing.level = target_level
            existing.under_construction = True
            existing.construction_turns_remaining = turns
            existing.save(update_fields=["level", "under_construction", "construction_turns_remaining"])
            building = existing
        else:
            building = Building.objects.create(
                province=province,
                building_type=building_type,
                level=target_level,
                is_active=True,
                under_construction=True,
                construction_turns_remaining=turns,
            )

        return Response(BuildingSerializer(building).data, status=status.HTTP_201_CREATED)


class AirZoneListView(generics.ListAPIView):
    serializer_class = AirZoneSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return AirZone.objects.filter(game_id=self.kwargs["game_id"]).prefetch_related("adjacent_air_zones")


class SeaZoneListView(generics.ListAPIView):
    serializer_class = SeaZoneSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return SeaZone.objects.filter(game_id=self.kwargs["game_id"]).prefetch_related(
            "adjacent_sea_zones", "adjacent_air_zones", "river_zones"
        )


class RiverZoneListView(generics.ListAPIView):
    serializer_class = RiverZoneSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return RiverZone.objects.filter(game_id=self.kwargs["game_id"]).prefetch_related(
            "adjacent_river_zones", "adjacent_air_zones"
        )
