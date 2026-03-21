from django.contrib import admin

from .models import Nation, NationModifier, NationPolicy


@admin.register(Nation)
class NationAdmin(admin.ModelAdmin):
    list_display = (
        "name", "game", "player",
        "gov_direction", "gov_economic_category", "gov_structure",
        "gov_power_origin", "gov_power_type",
        "get_strong_trait", "is_alive",
    )
    list_filter = (
        "is_alive",
        "gov_direction", "gov_economic_category", "gov_structure",
        "gov_power_origin", "gov_power_type",
    )
    search_fields = ("name", "player__username")

    @admin.display(description="Strong Trait")
    def get_strong_trait(self, obj):
        traits = obj.ideology_traits
        if isinstance(traits, dict):
            return traits.get("strong", "-")
        return "-"


@admin.register(NationPolicy)
class NationPolicyAdmin(admin.ModelAdmin):
    list_display = ("nation", "category", "level", "changed_turn")
    list_filter = ("category",)
    search_fields = ("nation__name",)


@admin.register(NationModifier)
class NationModifierAdmin(admin.ModelAdmin):
    list_display = ("name", "nation", "category", "target", "modifier_type", "value", "source")
    list_filter = ("category", "modifier_type", "source")
    search_fields = ("name", "nation__name")
