"""Espionage system views."""

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from games.models import Game
from nations.models import Nation

from .constants import FOREIGN_ACTION_TYPES
from .models import EspionageAction, EspionageState, IntelligenceSharing
from .serializers import (
    EspionageActionSerializer,
    EspionageOverviewSerializer,
    EspionageSlotSerializer,
    EspionageTargetDetailSerializer,
    IntelligenceSharingSerializer,
    IntelligenceSharingToggleSerializer,
)
from .slots import (
    get_action_type_slots,
    get_foreign_target_slots,
    get_suppress_slots,
    get_used_slots,
)


def _get_nation(request, game_id):
    """Resolve the authenticated user's living nation in the game.

    Returns (nation, None) on success or (None, Response) on failure.
    """
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return None, Response(
            {"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND
        )
    try:
        nation = Nation.objects.get(game=game, player=request.user, is_alive=True)
    except Nation.DoesNotExist:
        return None, Response(
            {"detail": "You do not have a living nation in this game."},
            status=status.HTTP_403_FORBIDDEN,
        )
    return nation, None


class EspionageOverviewView(APIView):
    """GET: Nation's espionage overview (attack, defense, transparency per target)."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id):
        nation, err = _get_nation(request, game_id)
        if err:
            return err

        states = EspionageState.objects.filter(
            game_id=game_id, attacker=nation
        ).select_related("target")

        data = []
        for state in states:
            data.append({
                "target_nation_id": state.target_id,
                "target_nation_name": state.target.name,
                "national_attack": state.national_attack,
                "national_defense": state.national_defense,
                "transparency": state.transparency,
            })

        serializer = EspionageOverviewSerializer(data, many=True)
        return Response(serializer.data)


class EspionageTargetDetailView(APIView):
    """GET: Revealed info for a specific target nation."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id, target_nation_id):
        nation, err = _get_nation(request, game_id)
        if err:
            return err

        try:
            state = EspionageState.objects.get(
                game_id=game_id, attacker=nation, target_id=target_nation_id
            )
        except EspionageState.DoesNotExist:
            return Response(
                {"detail": "No espionage data for this target."},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = {
            "target_nation_id": state.target_id,
            "transparency": state.transparency,
            "revealed_info": state.revealed_info,
        }
        serializer = EspionageTargetDetailSerializer(data)
        return Response(serializer.data)


class IntelligenceSharingView(APIView):
    """GET/POST: Manage voluntary intelligence sharing toggles."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id):
        nation, err = _get_nation(request, game_id)
        if err:
            return err

        shares = IntelligenceSharing.objects.filter(
            game_id=game_id, source_nation=nation
        )
        serializer = IntelligenceSharingSerializer(shares, many=True)
        return Response(serializer.data)

    def post(self, request, game_id):
        nation, err = _get_nation(request, game_id)
        if err:
            return err

        toggle_serializer = IntelligenceSharingToggleSerializer(data=request.data)
        toggle_serializer.is_valid(raise_exception=True)
        data = toggle_serializer.validated_data

        viewer_nation_id = data["viewer_nation_id"]
        category = data["category"]
        is_shared = data["is_shared"]

        # Validate viewer nation exists and is alive
        if not Nation.objects.filter(
            pk=viewer_nation_id, game_id=game_id, is_alive=True
        ).exists():
            return Response(
                {"detail": "Viewer nation not found or not alive."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if viewer_nation_id == nation.id:
            return Response(
                {"detail": "Cannot share intelligence with yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sharing, created = IntelligenceSharing.objects.update_or_create(
            game_id=game_id,
            source_nation=nation,
            viewer_nation_id=viewer_nation_id,
            category=category,
            defaults={"is_shared": is_shared},
        )

        serializer = IntelligenceSharingSerializer(sharing)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class EspionageActionListView(APIView):
    """GET: List active espionage actions for the requesting nation."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id):
        nation, err = _get_nation(request, game_id)
        if err:
            return err

        actions = EspionageAction.objects.filter(
            game_id=game_id,
            nation=nation,
            status=EspionageAction.Status.ACTIVE,
        ).select_related("target_nation", "target_province")

        serializer = EspionageActionSerializer(actions, many=True)
        return Response(serializer.data)


class EspionageSlotView(APIView):
    """GET: Available/used slots for foreign targets, per-action-type, and suppress."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id):
        nation, err = _get_nation(request, game_id)
        if err:
            return err

        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return Response(
                {"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND
            )

        used = get_used_slots(nation, game)

        action_type_slots = {}
        for action_type in FOREIGN_ACTION_TYPES:
            action_type_slots[action_type] = get_action_type_slots(nation, action_type)

        data = {
            "foreign_target_slots": get_foreign_target_slots(nation),
            "foreign_targets_used": len(used["foreign_targets"]),
            "foreign_targets_list": list(used["foreign_targets"]),
            "action_type_slots": action_type_slots,
            "action_type_used": used["by_type"],
            "suppress_slots": get_suppress_slots(nation),
            "suppress_used": used["suppress"],
        }

        serializer = EspionageSlotSerializer(data)
        return Response(serializer.data)
