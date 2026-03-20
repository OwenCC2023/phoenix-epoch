from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from games.models import Game, GameMembership

from .models import Nation, NationPolicy
from .serializers import NationCreateSerializer, NationPolicySerializer, NationSerializer


class NationListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/games/{game_id}/nations/      - List nations in a game
    POST /api/games/{game_id}/nations/      - Create a nation
    """

    def get_queryset(self):
        return Nation.objects.filter(game_id=self.kwargs["game_id"]).select_related(
            "game", "player"
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return NationCreateSerializer
        return NationSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        game_id = self.kwargs["game_id"]

        # Validate game exists and is in an appropriate status
        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return Response(
                {"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if game.status not in (Game.Status.LOBBY, Game.Status.ACTIVE):
            return Response(
                {"detail": "Nations can only be created in lobby or active games."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Must be a member of the game
        if not GameMembership.objects.filter(game=game, user=request.user).exists():
            return Response(
                {"detail": "You must be a member of this game to create a nation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Check if player already has a nation in this game
        if Nation.objects.filter(game=game, player=request.user).exists():
            return Response(
                {"detail": "You already have a nation in this game."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)


class NationDetailView(generics.RetrieveUpdateAPIView):
    """
    GET   /api/games/{game_id}/nations/{pk}/  - Retrieve nation details
    PATCH /api/games/{game_id}/nations/{pk}/  - Update nation (owner only)
    """

    serializer_class = NationSerializer

    def get_queryset(self):
        return Nation.objects.filter(game_id=self.kwargs["game_id"]).select_related(
            "game", "player"
        )

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        nation = self.get_object()
        if nation.player != request.user:
            return Response(
                {"detail": "Only the nation owner can update this nation."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)


class NationResourcesView(APIView):
    """GET /api/games/{game_id}/nations/{pk}/resources/ - Nation resource pool."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id, pk):
        return Response(
            {"detail": "Coming soon."}, status=status.HTTP_404_NOT_FOUND
        )


class NationProvincesView(APIView):
    """GET /api/games/{game_id}/nations/{pk}/provinces/ - Provinces owned by nation."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id, pk):
        return Response([], status=status.HTTP_200_OK)


class NationPolicyListView(generics.ListAPIView):
    """GET /api/games/{game_id}/nations/{pk}/policies/ - All policies for a nation."""

    serializer_class = NationPolicySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NationPolicy.objects.filter(
            nation_id=self.kwargs["pk"],
            nation__game_id=self.kwargs["game_id"],
        ).order_by("category")


class NationMilitaryGroupsView(generics.ListAPIView):
    """
    GET /api/games/{game_id}/nations/{pk}/military/groups/
    Returns all MilitaryGroups for the nation with nested formations and units.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id, pk):
        from provinces.models import MilitaryGroup
        from provinces.serializers import MilitaryGroupSerializer

        groups = (
            MilitaryGroup.objects
            .filter(nation_id=pk, nation__game_id=game_id)
            .prefetch_related("formations__units")
        )
        serializer = MilitaryGroupSerializer(groups, many=True)
        return Response(serializer.data)


class NationFormationsView(generics.ListAPIView):
    """
    GET /api/games/{game_id}/nations/{pk}/military/formations/
    Returns all Formations for the nation (with nested units).
    Optional ?domain=army|navy|air filter.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id, pk):
        from provinces.models import Formation
        from provinces.serializers import FormationSerializer

        qs = (
            Formation.objects
            .filter(nation_id=pk, nation__game_id=game_id)
            .prefetch_related("units")
            .select_related("province", "group")
        )
        domain = request.query_params.get("domain")
        if domain:
            qs = qs.filter(domain=domain)
        serializer = FormationSerializer(qs, many=True)
        return Response(serializer.data)
