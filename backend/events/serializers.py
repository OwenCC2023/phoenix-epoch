from rest_framework import serializers

from .models import GameEvent
from .templates import EVENT_TEMPLATES


class GameEventSerializer(serializers.ModelSerializer):
    """Read-only serializer for game events."""

    class Meta:
        model = GameEvent
        fields = [
            "id",
            "game",
            "title",
            "description",
            "scope",
            "effects",
            "affected_nations",
            "triggered_by",
            "turn_number",
            "expires_turn",
            "created_at",
        ]
        read_only_fields = fields


class GameEventCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating game events (GM only)."""

    affected_nation_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False, default=list
    )

    class Meta:
        model = GameEvent
        fields = [
            "title",
            "description",
            "scope",
            "effects",
            "affected_nation_ids",
            "expires_turn",
        ]

    def create(self, validated_data):
        affected_nation_ids = validated_data.pop("affected_nation_ids", [])
        game = self.context["game"]
        request = self.context["request"]

        event = GameEvent.objects.create(
            game=game,
            turn_number=game.current_turn_number,
            triggered_by=request.user,
            **validated_data,
        )

        if affected_nation_ids:
            from nations.models import Nation
            nations = Nation.objects.filter(id__in=affected_nation_ids, game=game)
            event.affected_nations.set(nations)

        return event


class EventTemplateSerializer(serializers.Serializer):
    """Serializer for listing available event templates."""

    name = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    scope = serializers.CharField()
