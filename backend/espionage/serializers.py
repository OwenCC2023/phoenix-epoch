"""Espionage system serializers."""

from rest_framework import serializers

from .models import EspionageState, EspionageAction, IntelligenceSharing


class EspionageOverviewSerializer(serializers.Serializer):
    """Per-target summary for the requesting nation."""
    target_nation_id = serializers.IntegerField()
    target_nation_name = serializers.CharField()
    national_attack = serializers.FloatField()
    national_defense = serializers.FloatField()
    transparency = serializers.FloatField()


class EspionageTargetDetailSerializer(serializers.Serializer):
    """Revealed information for a specific target nation."""
    target_nation_id = serializers.IntegerField()
    transparency = serializers.FloatField()
    revealed_info = serializers.JSONField()


class IntelligenceSharingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntelligenceSharing
        fields = ["id", "viewer_nation", "category", "is_shared"]
        read_only_fields = ["id"]


class IntelligenceSharingToggleSerializer(serializers.Serializer):
    """Toggle a sharing setting."""
    viewer_nation_id = serializers.IntegerField()
    category = serializers.ChoiceField(choices=IntelligenceSharing.Category.choices)
    is_shared = serializers.BooleanField()


class EspionageActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EspionageAction
        fields = [
            "id", "action_type", "target_nation", "target_province",
            "target_building_type", "status", "started_turn", "expires_turn",
            "result",
        ]


class EspionageSlotSerializer(serializers.Serializer):
    """Slot availability summary."""
    foreign_target_slots = serializers.IntegerField()
    foreign_targets_used = serializers.IntegerField()
    foreign_targets_list = serializers.ListField(child=serializers.IntegerField())
    action_type_slots = serializers.DictField(child=serializers.IntegerField())
    action_type_used = serializers.DictField(child=serializers.IntegerField())
    suppress_slots = serializers.IntegerField()
    suppress_used = serializers.IntegerField()
