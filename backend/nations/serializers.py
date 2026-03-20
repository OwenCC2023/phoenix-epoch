from rest_framework import serializers

from .helpers import apply_government_modifiers, create_default_policies
from .models import Nation, NationModifier, NationPolicy
from .trait_constants import validate_trait_selection


class NationModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationModifier
        fields = "__all__"
        read_only_fields = fields


class NationPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = NationPolicy
        fields = ["id", "category", "level", "changed_turn"]
        read_only_fields = ["id", "changed_turn"]


class NationSerializer(serializers.ModelSerializer):
    modifiers = NationModifierSerializer(many=True, read_only=True)
    policies = NationPolicySerializer(many=True, read_only=True)

    class Meta:
        model = Nation
        fields = [
            "id",
            "game",
            "player",
            "name",
            "description",
            "government_type",
            "ideology_traits",
            "motto",
            "is_alive",
            "created_at",
            "modifiers",
            "policies",
        ]
        read_only_fields = ["id", "game", "player", "is_alive", "created_at"]


class NationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nation
        fields = ["name", "description", "government_type", "ideology_traits", "motto"]

    def validate_government_type(self, value):
        from economy.constants import GOVERNMENT_TYPES

        if value not in GOVERNMENT_TYPES:
            valid = ", ".join(GOVERNMENT_TYPES.keys())
            raise serializers.ValidationError(
                f"Invalid government type. Choose from: {valid}"
            )
        return value

    def validate_ideology_traits(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("ideology_traits must be a JSON object")

        strong = value.get("strong")
        weak = value.get("weak")

        if not strong or not weak:
            raise serializers.ValidationError(
                'ideology_traits must have "strong" (string) and "weak" (list of 2 strings)'
            )

        try:
            validate_trait_selection(strong, weak)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

        return value

    def create(self, validated_data):
        game_id = self.context["view"].kwargs["game_id"]
        player = self.context["request"].user
        nation = Nation.objects.create(game_id=game_id, player=player, **validated_data)
        apply_government_modifiers(nation)
        create_default_policies(nation)
        return nation

    def to_representation(self, instance):
        return NationSerializer(instance, context=self.context).data
