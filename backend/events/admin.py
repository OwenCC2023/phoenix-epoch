from django.contrib import admin

from .models import GameEvent


@admin.register(GameEvent)
class GameEventAdmin(admin.ModelAdmin):
    list_display = ("title", "game", "scope", "turn_number", "created_at")
    list_filter = ("scope", "game")
    search_fields = ("title", "description")
