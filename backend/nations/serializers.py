from rest_framework import serializers

from .helpers import apply_government_modifiers, create_default_policies
from .models import Nation, NationDPPool, NationMilitaryDP, NationModifier, NationPolicy
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


class NationDPPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationDPPool
        fields = ["available_points", "last_grant_turn"]


class NationMilitaryDPSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationMilitaryDP
        fields = ["category", "points"]


class NationSerializer(serializers.ModelSerializer):
    modifiers = NationModifierSerializer(many=True, read_only=True)
    policies = NationPolicySerializer(many=True, read_only=True)
    dp_pool = NationDPPoolSerializer(read_only=True)
    military_dp = NationMilitaryDPSerializer(many=True, read_only=True)
    provincial_dp_summary = serializers.SerializerMethodField()

    def get_provincial_dp_summary(self, nation):
        """Sum of all provincial DP per category across this nation's provinces.

        Display only — no mechanical effect. Returns {category: total_points}.
        """
        from provinces.models import ProvinceDevelopmentPoints
        from django.db.models import Sum
        rows = (
            ProvinceDevelopmentPoints.objects
            .filter(province__nation=nation)
            .values("category")
            .annotate(total=Sum("points"))
        )
        return {row["category"]: row["total"] for row in rows}

    class Meta:
        model = Nation
        fields = [
            "id",
            "game",
            "player",
            "name",
            "description",
            "gov_direction",
            "gov_economic_category",
            "gov_structure",
            "gov_power_origin",
            "gov_power_type",
            "ideology_traits",
            "motto",
            "is_alive",
            "created_at",
            "modifiers",
            "policies",
            "dp_pool",
            "military_dp",
            "provincial_dp_summary",
        ]
        read_only_fields = ["id", "game", "player", "is_alive", "created_at"]


class NationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nation
        fields = [
            "name",
            "description",
            "gov_direction",
            "gov_economic_category",
            "gov_structure",
            "gov_power_origin",
            "gov_power_type",
            "ideology_traits",
            "motto",
        ]

    def _validate_gov_component(self, component_key, value):
        from nations.government_constants import GOV_COMPONENTS
        options = GOV_COMPONENTS[component_key]
        if value not in options:
            valid = ", ".join(options.keys())
            raise serializers.ValidationError(
                f"Invalid value '{value}'. Choose from: {valid}"
            )
        return value

    def validate_gov_direction(self, value):
        return self._validate_gov_component("direction", value)

    def validate_gov_economic_category(self, value):
        return self._validate_gov_component("economic_category", value)

    def validate_gov_structure(self, value):
        return self._validate_gov_component("structure", value)

    def validate_gov_power_origin(self, value):
        return self._validate_gov_component("power_origin", value)

    def validate_gov_power_type(self, value):
        return self._validate_gov_component("power_type", value)

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
