"""Trade system serializers."""

from rest_framework import serializers
from .models import TradeRoute, CapitalRelocation


class TradeRouteSerializer(serializers.ModelSerializer):
    from_nation_name = serializers.CharField(source="from_nation.name", read_only=True)
    to_nation_name = serializers.CharField(source="to_nation.name", read_only=True)

    class Meta:
        model = TradeRoute
        fields = [
            "id",
            "from_nation",
            "from_nation_name",
            "to_nation",
            "to_nation_name",
            "good",
            "quantity_per_turn",
            "domain_mode",
            "status",
            "path_nodes",
            "total_length",
            "capacity_by_domain",
            "arrival_turns",
            "in_flight",
            "created_turn",
        ]
        read_only_fields = fields


class CapitalRelocationSerializer(serializers.ModelSerializer):
    target_province_name = serializers.CharField(source="target_province.name", read_only=True)

    class Meta:
        model = CapitalRelocation
        fields = [
            "id",
            "target_province",
            "target_province_name",
            "started_turn",
            "completes_turn",
            "cost_paid",
        ]
        read_only_fields = fields


class TradeRoutePreviewSerializer(serializers.Serializer):
    """Response schema for the route preview endpoint."""
    path_nodes = serializers.ListField(child=serializers.ListField())
    total_length = serializers.FloatField()
    domain_segments = serializers.DictField(child=serializers.FloatField())
    arrival_turns = serializers.IntegerField()
    capacity_consumed = serializers.DictField(child=serializers.FloatField())
    capacity_available = serializers.DictField(child=serializers.FloatField())
    capacity_used = serializers.DictField(child=serializers.FloatField())
    path_exists = serializers.BooleanField()
