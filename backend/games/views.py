from django.utils import timezone
from datetime import timedelta

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Game, GameMembership
from .permissions import IsGameCreator, IsGameMember
from .serializers import GameCreateSerializer, GameMembershipSerializer, GameSerializer


class GameListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/games/       - List all games
    POST /api/games/       - Create a new game
    """

    queryset = Game.objects.all().order_by("-created_at")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return GameCreateSerializer
        return GameSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class GameDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/games/{id}/  - Retrieve game details
    PATCH  /api/games/{id}/  - Update game (creator only)
    DELETE /api/games/{id}/  - Delete game (creator only)
    """

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsGameCreator()]


class GameJoinView(APIView):
    """POST /api/games/{id}/join/ - Join a game as a player."""

    def post(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response({"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        if game.status != Game.Status.LOBBY:
            return Response(
                {"detail": "Can only join games in lobby status."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if game.memberships.count() >= game.max_players:
            return Response(
                {"detail": "Game is full."}, status=status.HTTP_400_BAD_REQUEST
            )

        membership, created = GameMembership.objects.get_or_create(
            game=game, user=request.user, defaults={"role": GameMembership.Role.PLAYER}
        )
        if not created:
            return Response(
                {"detail": "You are already in this game."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            GameMembershipSerializer(membership).data, status=status.HTTP_201_CREATED
        )


class GameLeaveView(APIView):
    """POST /api/games/{id}/leave/ - Leave a game."""

    def post(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response({"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            membership = GameMembership.objects.get(game=game, user=request.user)
        except GameMembership.DoesNotExist:
            return Response(
                {"detail": "You are not in this game."}, status=status.HTTP_400_BAD_REQUEST
            )

        if game.creator == request.user:
            return Response(
                {"detail": "The creator cannot leave. Delete the game instead."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GameStartView(APIView):
    """POST /api/games/{id}/start/ - Start the game (creator/gm only)."""

    def post(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response({"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user != game.creator and request.user != game.gm:
            return Response(
                {"detail": "Only the creator or GM can start the game."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if game.status != Game.Status.LOBBY:
            return Response(
                {"detail": "Game is not in lobby status."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        player_count = game.memberships.filter(role=GameMembership.Role.PLAYER).count()
        gm_count = game.memberships.filter(role=GameMembership.Role.GM).count()
        total = player_count + gm_count

        if total < game.min_players:
            return Response(
                {"detail": f"Need at least {game.min_players} players to start."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        game.status = Game.Status.ACTIVE
        game.current_turn_number = 1
        game.current_turn_deadline = timezone.now() + timedelta(hours=game.turn_duration_hours)
        game.save()

        from economy.whitespace import initialize_whitespace
        initialize_whitespace(game)

        return Response(GameSerializer(game).data, status=status.HTTP_200_OK)


class GameMembersView(generics.ListAPIView):
    """GET /api/games/{id}/members/ - List members of a game."""

    serializer_class = GameMembershipSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return GameMembership.objects.filter(game_id=self.kwargs["pk"]).select_related("user")


class GamePauseView(APIView):
    """POST /api/games/{id}/admin/pause/ - Pause a game (GM only)."""

    def post(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response({"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        membership = GameMembership.objects.filter(game=game, user=request.user, role="gm").first()
        if not membership and game.creator != request.user:
            return Response({"detail": "GM access required."}, status=status.HTTP_403_FORBIDDEN)

        if game.status != Game.Status.ACTIVE:
            return Response({"detail": "Game is not active."}, status=status.HTTP_400_BAD_REQUEST)

        game.status = Game.Status.PAUSED
        game.save(update_fields=["status"])

        from .notifications import notify_game_paused
        notify_game_paused(game.id)

        return Response(GameSerializer(game).data)


class GameResumeView(APIView):
    """POST /api/games/{id}/admin/resume/ - Resume a paused game (GM only)."""

    def post(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response({"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        membership = GameMembership.objects.filter(game=game, user=request.user, role="gm").first()
        if not membership and game.creator != request.user:
            return Response({"detail": "GM access required."}, status=status.HTTP_403_FORBIDDEN)

        if game.status != Game.Status.PAUSED:
            return Response({"detail": "Game is not paused."}, status=status.HTTP_400_BAD_REQUEST)

        game.status = Game.Status.ACTIVE
        new_deadline = timezone.now() + timedelta(hours=game.turn_duration_hours)
        game.current_turn_deadline = new_deadline
        game.save(update_fields=["status", "current_turn_deadline"])

        from .notifications import notify_game_resumed
        notify_game_resumed(game.id, new_deadline)

        return Response(GameSerializer(game).data)


class GameForceResolveView(APIView):
    """POST /api/games/{id}/admin/force-resolve/ - Force resolve current turn (GM only)."""

    def post(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response({"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        membership = GameMembership.objects.filter(game=game, user=request.user, role="gm").first()
        if not membership and game.creator != request.user:
            return Response({"detail": "GM access required."}, status=status.HTTP_403_FORBIDDEN)

        from turns.tasks import resolve_turn
        resolve_turn.delay(game.id)

        return Response({"detail": "Turn resolution triggered."})


class GameAdminOverviewView(APIView):
    """GET /api/games/{id}/admin/overview/ - Get full game state (GM only)."""

    def get(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response({"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        membership = GameMembership.objects.filter(game=game, user=request.user, role="gm").first()
        if not membership and game.creator != request.user:
            return Response({"detail": "GM access required."}, status=status.HTTP_403_FORBIDDEN)

        from nations.models import Nation
        from economy.models import NationResourcePool

        nations_data = []
        for nation in Nation.objects.filter(game=game):
            pool = NationResourcePool.objects.filter(nation=nation).first()
            nations_data.append({
                "id": nation.id,
                "name": nation.name,
                "player": nation.player.username,
                "gov_direction": nation.gov_direction,
                "gov_economic_category": nation.gov_economic_category,
                "gov_structure": nation.gov_structure,
                "gov_power_origin": nation.gov_power_origin,
                "gov_power_type": nation.gov_power_type,
                "ideology_traits": nation.ideology_traits,
                "is_alive": nation.is_alive,
                "provinces": nation.provinces.count(),
                "resources": {
                    "food": pool.food if pool else 0,
                    "materials": pool.materials if pool else 0,
                    "energy": pool.energy if pool else 0,
                    "wealth": pool.wealth if pool else 0,
                    "manpower": pool.manpower if pool else 0,
                    "research": pool.research if pool else 0,
                    "stability": pool.stability if pool else 50,
                    "total_population": pool.total_population if pool else 0,
                } if pool else None,
            })

        from turns.models import Turn, TurnSubmission
        current_turn = Turn.objects.filter(game=game, status="pending").first()
        submissions = []
        if current_turn:
            for sub in TurnSubmission.objects.filter(turn=current_turn).select_related("nation"):
                submissions.append({
                    "nation": sub.nation.name,
                    "submitted_at": sub.submitted_at.isoformat(),
                })

        return Response({
            "game": GameSerializer(game).data,
            "nations": nations_data,
            "current_turn": {
                "turn_number": current_turn.turn_number if current_turn else None,
                "deadline": current_turn.deadline.isoformat() if current_turn else None,
                "submissions": submissions,
            },
        })
