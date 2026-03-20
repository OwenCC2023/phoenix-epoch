from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for Phoenix Epoch."""

    display_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    games_played = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.display_name or self.username
