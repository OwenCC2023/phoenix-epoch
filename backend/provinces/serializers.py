from rest_framework import serializers

from .models import (
    AirZone, Building, Formation, MilitaryGroup, MilitaryUnit,
    Province, ProvinceResources, ProvinceSectorAllocation, RiverZone, SeaZone,
)


class ProvinceResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvinceResources
        fields = "__all__"


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = [
            "id",
            "province",
            "building_type",
            "level",
            "is_active",
            "under_construction",
            "construction_turns_remaining",
        ]
        read_only_fields = ["id", "province", "level", "under_construction", "construction_turns_remaining"]


class AirZoneSerializer(serializers.ModelSerializer):
    adjacent_air_zone_ids = serializers.PrimaryKeyRelatedField(
        source="adjacent_air_zones", many=True, read_only=True
    )

    class Meta:
        model = AirZone
        fields = ["id", "game", "name", "adjacent_air_zone_ids"]


class SeaZoneSerializer(serializers.ModelSerializer):
    adjacent_sea_zone_ids = serializers.PrimaryKeyRelatedField(
        source="adjacent_sea_zones", many=True, read_only=True
    )
    adjacent_air_zone_ids = serializers.PrimaryKeyRelatedField(
        source="adjacent_air_zones", many=True, read_only=True
    )
    river_zone_ids = serializers.PrimaryKeyRelatedField(
        source="river_zones", many=True, read_only=True
    )

    class Meta:
        model = SeaZone
        fields = ["id", "game", "name", "adjacent_sea_zone_ids", "adjacent_air_zone_ids", "river_zone_ids"]


class RiverZoneSerializer(serializers.ModelSerializer):
    adjacent_river_zone_ids = serializers.PrimaryKeyRelatedField(
        source="adjacent_river_zones", many=True, read_only=True
    )
    adjacent_air_zone_ids = serializers.PrimaryKeyRelatedField(
        source="adjacent_air_zones", many=True, read_only=True
    )

    class Meta:
        model = RiverZone
        fields = ["id", "game", "name", "sea_zone", "adjacent_river_zone_ids", "adjacent_air_zone_ids"]


class ProvinceSerializer(serializers.ModelSerializer):
    resources = ProvinceResourcesSerializer(read_only=True)
    buildings = BuildingSerializer(many=True, read_only=True)
    adjacent_province_ids = serializers.PrimaryKeyRelatedField(
        source="adjacent_provinces", many=True, read_only=True
    )
    adjacent_sea_zone_ids = serializers.PrimaryKeyRelatedField(
        source="adjacent_sea_zones", many=True, read_only=True
    )
    adjacent_river_zone_ids = serializers.PrimaryKeyRelatedField(
        source="adjacent_river_zones", many=True, read_only=True
    )

    class Meta:
        model = Province
        fields = [
            "id",
            "game",
            "nation",
            "name",
            "terrain_type",
            "population",
            "local_stability",
            "local_security",
            "local_happiness",
            "literacy",
            "designation",
            "is_capital",
            "is_coastal",
            "is_river",
            "center_x",
            "center_y",
            "sea_border_distance",
            "river_border_distance",
            "air_zone",
            "adjacent_province_ids",
            "adjacent_sea_zone_ids",
            "adjacent_river_zone_ids",
            "created_at",
            "resources",
            "buildings",
        ]


class ProvinceSectorAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvinceSectorAllocation
        fields = ["sector", "percentage"]

    def validate_percentage(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Percentage must be between 0 and 100.")
        return value


class MilitaryUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilitaryUnit
        fields = [
            "id",
            "formation",
            "unit_type",
            "quantity",
            "quantity_in_training",
            "construction_turns_remaining",
            "is_active",
            "quantity_in_transit",
            "transit_turns_remaining",
            "training_province",
        ]
        read_only_fields = fields


class FormationSerializer(serializers.ModelSerializer):
    units = MilitaryUnitSerializer(many=True, read_only=True)

    class Meta:
        model = Formation
        fields = [
            "id",
            "nation",
            "group",
            "province",
            "name",
            "domain",
            "formation_type",
            "effective_strength",
            "units",
        ]
        read_only_fields = ["id", "nation", "effective_strength"]


class MilitaryGroupSerializer(serializers.ModelSerializer):
    formations = FormationSerializer(many=True, read_only=True)

    class Meta:
        model = MilitaryGroup
        fields = ["id", "nation", "name", "formations"]
        read_only_fields = ["id", "nation"]


class ProvinceSectorAllocationBulkSerializer(serializers.Serializer):
    allocations = serializers.ListField(
        child=serializers.DictField(),
        min_length=6,
        max_length=6,
    )

    VALID_SECTORS = {"agriculture", "industry", "energy", "commerce", "military", "research"}

    def validate_allocations(self, value):
        # Validate all 6 sectors are present
        sectors_seen = set()
        total = 0

        for item in value:
            if "sector" not in item or "percentage" not in item:
                raise serializers.ValidationError(
                    "Each allocation must have 'sector' and 'percentage' keys."
                )

            sector = item["sector"]
            percentage = item["percentage"]

            if sector not in self.VALID_SECTORS:
                raise serializers.ValidationError(
                    f"Invalid sector '{sector}'. Must be one of: {', '.join(sorted(self.VALID_SECTORS))}"
                )

            if sector in sectors_seen:
                raise serializers.ValidationError(f"Duplicate sector '{sector}'.")
            sectors_seen.add(sector)

            if not isinstance(percentage, int) or percentage < 0 or percentage > 100:
                raise serializers.ValidationError(
                    f"Percentage for '{sector}' must be an integer between 0 and 100."
                )

            total += percentage

        if sectors_seen != self.VALID_SECTORS:
            missing = self.VALID_SECTORS - sectors_seen
            raise serializers.ValidationError(
                f"Missing sectors: {', '.join(sorted(missing))}"
            )

        if total != 100:
            raise serializers.ValidationError(
                f"Allocations must sum to 100, got {total}."
            )

        return value
