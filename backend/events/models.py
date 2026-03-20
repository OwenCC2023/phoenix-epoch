from django.conf import settings
from django.db import models


class GameEvent(models.Model):
    """An event triggered in a game (by GM or system)."""

    class Scope(models.TextChoices):
        GLOBAL = "global", "Global"
        TARGETED = "targeted", "Targeted"

    game = models.ForeignKey("games.Game", on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    scope = models.CharField(max_length=10, choices=Scope.choices, default=Scope.GLOBAL)
    effects = models.JSONField(default=dict)
    affected_nations = models.ManyToManyField("nations.Nation", blank=True, related_name="events")
    triggered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    turn_number = models.PositiveIntegerField()
    expires_turn = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (Turn {self.turn_number})"
