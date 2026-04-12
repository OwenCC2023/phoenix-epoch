from rest_framework import serializers

from .models import NationGoodStock, NationResourcePool, ResourceLedger, ProvinceLedger


VALID_RESOURCE_KEYS = {"food", "materials", "energy", "wealth", "manpower", "research"}


class ConstructionBuildingSerializer(serializers.Serializer):
    """Read-only snapshot of a building that is under construction."""
    id = serializers.IntegerField()
    province = serializers.IntegerField(source="province.id")
    province_name = serializers.CharField(source="province.name")
    building_type = serializers.CharField()
    level = serializers.IntegerField()
    construction_turns_remaining = serializers.IntegerField()


class NationGoodStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationGoodStock
        fields = [
            "id", "nation",
            "consumer_goods", "arms", "fuel", "machinery",
            "chemicals", "medicine", "components", "heavy_equipment",
        ]
        read_only_fields = [
            "id", "nation",
            "consumer_goods", "arms", "fuel", "machinery",
            "chemicals", "medicine", "components", "heavy_equipment",
        ]


class NationResourcePoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationResourcePool
        fields = "__all__"
        read_only_fields = [f.name for f in NationResourcePool._meta.get_fields() if hasattr(f, "name")]


class ResourceLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceLedger
        fields = "__all__"
        read_only_fields = [f.name for f in ResourceLedger._meta.get_fields() if hasattr(f, "name")]


class ProvinceLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvinceLedger
        fields = "__all__"
        read_only_fields = [f.name for f in ProvinceLedger._meta.get_fields() if hasattr(f, "name")]


