from django.contrib import admin
from .models import EspionageState, EspionageAction, IntelligenceSharing, BranchOfficeSpecialization


@admin.register(EspionageState)
class EspionageStateAdmin(admin.ModelAdmin):
    list_display = ("attacker", "target", "national_attack", "national_defense", "transparency", "turn_updated")
    list_filter = ("game",)
    readonly_fields = ("revealed_info",)


@admin.register(EspionageAction)
class EspionageActionAdmin(admin.ModelAdmin):
    list_display = ("nation", "action_type", "target_nation", "target_province", "status", "started_turn", "expires_turn")
    list_filter = ("game", "status", "action_type")


@admin.register(IntelligenceSharing)
class IntelligenceSharingAdmin(admin.ModelAdmin):
    list_display = ("source_nation", "viewer_nation", "category", "is_shared")
    list_filter = ("game", "category", "is_shared")


@admin.register(BranchOfficeSpecialization)
class BranchOfficeSpecializationAdmin(admin.ModelAdmin):
    list_display = ("building", "action_type")
    list_filter = ("action_type",)
