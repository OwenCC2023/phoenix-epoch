from rest_framework import serializers

from .models import NationGoodStock, NationResourcePool, ResourceLedger, ProvinceLedger, TradeOffer


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


class TradeOfferSerializer(serializers.ModelSerializer):
    from_nation_name = serializers.CharField(source="from_nation.name", read_only=True)
    to_nation_name = serializers.CharField(source="to_nation.name", read_only=True)

    class Meta:
        model = TradeOffer
        fields = "__all__"
        read_only_fields = [f.name for f in TradeOffer._meta.get_fields() if hasattr(f, "name")]


class TradeOfferCreateSerializer(serializers.Serializer):
    to_nation = serializers.IntegerField()
    offering = serializers.DictField(child=serializers.FloatField())
    requesting = serializers.DictField(child=serializers.FloatField())

    def _validate_resource_dict(self, value, field_name):
        if not value:
            raise serializers.ValidationError(f"{field_name} must not be empty.")
        for key, amount in value.items():
            if key not in VALID_RESOURCE_KEYS:
                valid = ", ".join(sorted(VALID_RESOURCE_KEYS))
                raise serializers.ValidationError(
                    f"Invalid resource key '{key}' in {field_name}. Valid keys: {valid}"
                )
            if amount <= 0:
                raise serializers.ValidationError(
                    f"All values in {field_name} must be positive. Got {amount} for '{key}'."
                )
        return value

    def validate_offering(self, value):
        return self._validate_resource_dict(value, "offering")

    def validate_requesting(self, value):
        return self._validate_resource_dict(value, "requesting")

    def validate_to_nation(self, value):
        from nations.models import Nation

        try:
            Nation.objects.get(pk=value)
        except Nation.DoesNotExist:
            raise serializers.ValidationError("Target nation does not exist.")
        return value

    def create(self, validated_data):
        return TradeOffer.objects.create(**validated_data)

    def to_representation(self, instance):
        return TradeOfferSerializer(instance, context=self.context).data
