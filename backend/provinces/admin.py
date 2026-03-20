from django.contrib import admin

from .models import (
    AirZone, Building, Formation, MilitaryGroup, MilitaryUnit,
    Province, ProvinceResources, ProvinceSectorAllocation, RiverZone, SeaZone,
)


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("name", "game", "nation", "terrain_type", "population", "is_capital", "is_coastal", "is_river", "air_zone")
    list_filter = ("terrain_type", "is_capital", "is_coastal", "is_river", "air_zone")
    search_fields = ("name", "nation__name")
    filter_horizontal = ("adjacent_provinces", "adjacent_sea_zones", "adjacent_river_zones")


@admin.register(AirZone)
class AirZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "game")
    list_filter = ("game",)
    search_fields = ("name",)
    filter_horizontal = ("adjacent_air_zones",)


@admin.register(SeaZone)
class SeaZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "game")
    list_filter = ("game",)
    search_fields = ("name",)
    filter_horizontal = ("adjacent_sea_zones", "adjacent_air_zones")


@admin.register(RiverZone)
class RiverZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "game", "sea_zone")
    list_filter = ("game",)
    search_fields = ("name",)
    filter_horizontal = ("adjacent_river_zones", "adjacent_air_zones")


@admin.register(ProvinceResources)
class ProvinceResourcesAdmin(admin.ModelAdmin):
    list_display = ("province", "food", "materials", "energy", "wealth", "manpower", "research", "updated_turn")
    search_fields = ("province__name",)


@admin.register(ProvinceSectorAllocation)
class ProvinceSectorAllocationAdmin(admin.ModelAdmin):
    list_display = ("province", "sector", "percentage", "turn_number")
    list_filter = ("sector",)
    search_fields = ("province__name",)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ("province", "building_type", "level", "is_active", "under_construction", "construction_turns_remaining")
    list_filter = ("building_type", "is_active", "under_construction")
    search_fields = ("province__name",)


@admin.register(MilitaryGroup)
class MilitaryGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "nation")
    search_fields = ("name", "nation__name")


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ("name", "nation", "domain", "formation_type", "province", "group", "effective_strength")
    list_filter = ("domain", "formation_type")
    search_fields = ("name", "nation__name")


@admin.register(MilitaryUnit)
class MilitaryUnitAdmin(admin.ModelAdmin):
    list_display = (
        "unit_type", "formation", "quantity", "quantity_in_training",
        "construction_turns_remaining", "is_active", "training_province",
    )
    list_filter = ("unit_type", "is_active")
    search_fields = ("unit_type", "formation__name", "formation__nation__name")
