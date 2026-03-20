from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import Game, GameMembership


class GameMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GameMembership
        fields = ["id", "user", "role", "joined_at"]
        read_only_fields = ["id", "joined_at"]


class GameSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    gm = UserSerializer(read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            "id",
            "name",
            "description",
            "status",
            "creator",
            "gm",
            "max_players",
            "min_players",
            "turn_duration_hours",
            "current_turn_number",
            "current_turn_deadline",
            "starting_provinces",
            "member_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "creator",
            "gm",
            "current_turn_number",
            "current_turn_deadline",
            "created_at",
            "updated_at",
        ]

    def get_member_count(self, obj):
        return obj.memberships.count()


class GameCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "name",
            "description",
            "max_players",
            "min_players",
            "turn_duration_hours",
            "starting_provinces",
        ]

    def validate(self, data):
        if data.get("min_players", 2) > data.get("max_players", 30):
            raise serializers.ValidationError(
                {"min_players": "min_players cannot exceed max_players."}
            )
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        game = Game.objects.create(creator=user, gm=user, **validated_data)
        # Auto-add creator as a GM member
        GameMembership.objects.create(game=game, user=user, role=GameMembership.Role.GM)
        return game

    def to_representation(self, instance):
        return GameSerializer(instance, context=self.context).data
