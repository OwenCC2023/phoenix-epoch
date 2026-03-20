from django.conf import settings
from django.db import models


class Game(models.Model):
    """A single game lobby / session."""

    class Status(models.TextChoices):
        LOBBY = "lobby", "Lobby"
        ACTIVE = "active", "Active"
        PAUSED = "paused", "Paused"
        FINISHED = "finished", "Finished"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.LOBBY)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_games"
    )
    gm = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gm_games",
    )
    max_players = models.PositiveIntegerField(default=30)
    min_players = models.PositiveIntegerField(default=2)
    turn_duration_hours = models.PositiveIntegerField(default=24)
    current_turn_number = models.PositiveIntegerField(default=0)
    current_turn_deadline = models.DateTimeField(null=True, blank=True)
    starting_provinces = models.PositiveIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class GameMembership(models.Model):
    """Tracks which users belong to which games."""

    class Role(models.TextChoices):
        PLAYER = "player", "Player"
        GM = "gm", "GM"
        OBSERVER = "observer", "Observer"

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="game_memberships"
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.PLAYER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("game", "user")

    def __str__(self):
        return f"{self.user} in {self.game} ({self.role})"
