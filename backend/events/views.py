from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from games.models import Game, GameMembership

from .helpers import apply_event_to_nations
from .models import GameEvent
from .serializers import GameEventCreateSerializer, GameEventSerializer, EventTemplateSerializer
from .templates import EVENT_TEMPLATES


class GameEventListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/games/{game_id}/events/       - List events for a game
    POST /api/games/{game_id}/events/       - Create an event (GM only)
    """

    def get_serializer_class(self):
        if self.request.method == "POST":
            return GameEventCreateSerializer
        return GameEventSerializer

    def get_queryset(self):
        return GameEvent.objects.filter(game_id=self.kwargs["game_id"]).order_by("-created_at")

    def get_game(self):
        return Game.objects.get(pk=self.kwargs["game_id"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method == "POST":
            context["game"] = self.get_game()
        return context

    def create(self, request, *args, **kwargs):
        game = self.get_game()

        # GM-only check
        membership = GameMembership.objects.filter(game=game, user=request.user, role="gm").first()
        if not membership and game.creator != request.user:
            return Response({"detail": "GM access required."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()

        # Apply event effects to affected nations
        if event.scope == GameEvent.Scope.GLOBAL:
            from nations.models import Nation
            nations = Nation.objects.filter(game=game, is_alive=True)
            event.affected_nations.set(nations)
        else:
            nations = event.affected_nations.all()

        apply_event_to_nations(event, nations)

        # Send WebSocket notification
        from games.notifications import notify_event_triggered
        notify_event_triggered(game.id, event.id, event.title, event.description)

        return Response(GameEventSerializer(event).data, status=status.HTTP_201_CREATED)


class EventTemplateListView(APIView):
    """GET /api/games/{game_id}/events/templates/ - List available event templates (GM only)."""

    def get(self, request, game_id):
        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return Response({"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        membership = GameMembership.objects.filter(game=game, user=request.user, role="gm").first()
        if not membership and game.creator != request.user:
            return Response({"detail": "GM access required."}, status=status.HTTP_403_FORBIDDEN)

        templates = [
            {"name": name, "title": t["title"], "description": t["description"], "scope": t["scope"]}
            for name, t in EVENT_TEMPLATES.items()
        ]

        serializer = EventTemplateSerializer(templates, many=True)
        return Response(serializer.data)
