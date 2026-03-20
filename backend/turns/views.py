from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from games.models import Game
from nations.models import Nation

from .models import Turn, Order, TurnSubmission
from .serializers import (
    TurnSerializer,
    OrderSerializer,
    OrderCreateSerializer,
    TurnSubmissionSerializer,
)


class TurnListView(generics.ListAPIView):
    """GET /api/games/{game_id}/turns/ — List turns in a game."""

    serializer_class = TurnSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Turn.objects.filter(game_id=self.kwargs["game_id"])


class CurrentTurnView(generics.RetrieveAPIView):
    """GET /api/games/{game_id}/turns/current/ — Get current pending turn."""

    serializer_class = TurnSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        turn = Turn.objects.filter(
            game_id=self.kwargs["game_id"],
            status=Turn.Status.PENDING,
        ).order_by("-turn_number").first()

        if not turn:
            from django.http import Http404
            raise Http404("No pending turn found.")
        return turn


class OrderListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/games/{game_id}/turns/current/orders/ — List current orders for user's nation.
    POST /api/games/{game_id}/turns/current/orders/ — Create a new order.
    """

    permission_classes = [permissions.IsAuthenticated]

    def _get_current_turn(self):
        return Turn.objects.filter(
            game_id=self.kwargs["game_id"],
            status=Turn.Status.PENDING,
        ).order_by("-turn_number").first()

    def _get_nation(self):
        return Nation.objects.filter(
            game_id=self.kwargs["game_id"],
            player=self.request.user,
            is_alive=True,
        ).first()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        turn = self._get_current_turn()
        nation = self._get_nation()
        if not turn or not nation:
            return Order.objects.none()
        return Order.objects.filter(turn=turn, nation=nation)

    def create(self, request, *args, **kwargs):
        turn = self._get_current_turn()
        if not turn:
            return Response(
                {"detail": "No pending turn found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        nation = self._get_nation()
        if not nation:
            return Response(
                {"detail": "You do not have a living nation in this game."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(turn=turn, nation=nation)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubmitOrdersView(APIView):
    """POST /api/games/{game_id}/turns/current/submit/ — Submit orders for the current turn."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, game_id):
        turn = Turn.objects.filter(
            game_id=game_id,
            status=Turn.Status.PENDING,
        ).order_by("-turn_number").first()

        if not turn:
            return Response(
                {"detail": "No pending turn found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        nation = Nation.objects.filter(
            game_id=game_id,
            player=request.user,
            is_alive=True,
        ).first()

        if not nation:
            return Response(
                {"detail": "You do not have a living nation in this game."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Check if already submitted
        if TurnSubmission.objects.filter(turn=turn, nation=nation).exists():
            return Response(
                {"detail": "Orders already submitted for this turn."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Mark all draft orders as submitted
        draft_orders = Order.objects.filter(turn=turn, nation=nation, status=Order.Status.DRAFT)
        draft_orders.update(status=Order.Status.SUBMITTED)

        # Create submission record
        submission = TurnSubmission.objects.create(turn=turn, nation=nation)

        # Trigger early resolution check
        from .tasks import check_early_resolution
        check_early_resolution.delay(game_id)

        return Response(
            TurnSubmissionSerializer(submission).data,
            status=status.HTTP_201_CREATED,
        )


class TurnHistoryDetailView(generics.RetrieveAPIView):
    """GET /api/games/{game_id}/turns/{turn_number}/ — Get turn details by turn number."""

    serializer_class = TurnSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        from django.shortcuts import get_object_or_404
        return get_object_or_404(
            Turn,
            game_id=self.kwargs["game_id"],
            turn_number=self.kwargs["turn_number"],
        )
