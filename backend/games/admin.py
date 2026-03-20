from django.contrib import admin

from .models import Game, GameMembership


class GameMembershipInline(admin.TabularInline):
    model = GameMembership
    extra = 0


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ["name", "status", "creator", "max_players", "current_turn_number", "created_at"]
    list_filter = ["status"]
    inlines = [GameMembershipInline]


@admin.register(GameMembership)
class GameMembershipAdmin(admin.ModelAdmin):
    list_display = ["game", "user", "role", "joined_at"]
    list_filter = ["role"]
