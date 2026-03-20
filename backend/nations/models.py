from django.conf import settings
from django.db import models


class Nation(models.Model):
    game = models.ForeignKey("games.Game", on_delete=models.CASCADE, related_name="nations")
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="nations")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    government_type = models.CharField(max_length=30)
    ideology_traits = models.JSONField(
        default=dict,
        help_text='{"strong": "trait_key", "weak": ["trait_key", "trait_key"]}',
    )
    motto = models.CharField(max_length=200, blank=True)
    is_alive = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("game", "player")

    def __str__(self):
        return f"{self.name} ({self.game})"


class NationPolicy(models.Model):
    """A single policy setting for a nation (one row per category)."""

    nation = models.ForeignKey(Nation, on_delete=models.CASCADE, related_name="policies")
    category = models.CharField(max_length=50)   # key from POLICY_CATEGORIES
    level = models.PositiveSmallIntegerField()    # 0-indexed into levels list
    changed_turn = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("nation", "category")

    def __str__(self):
        return f"{self.nation.name}: {self.category} = {self.level}"


class NationModifier(models.Model):
    """Generic modifier applied at the national level."""

    class Category(models.TextChoices):
        ECONOMY = "economy"
        MILITARY = "military"
        STABILITY = "stability"
        DIPLOMACY = "diplomacy"
        GROWTH = "growth"
        BUILDING_EFFICIENCY = "building_efficiency"   # target = category name or "all"

    class ModifierType(models.TextChoices):
        FLAT = "flat"
        PERCENTAGE = "percentage"

    class Source(models.TextChoices):
        GOVERNMENT = "government"
        TRAIT = "trait"
        EVENT = "event"
        POLICY = "policy"
        TRADE = "trade"

    nation = models.ForeignKey(Nation, on_delete=models.CASCADE, related_name="modifiers")
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=Category.choices)
    target = models.CharField(max_length=50)  # which resource or stat
    modifier_type = models.CharField(max_length=15, choices=ModifierType.choices)
    value = models.FloatField()
    source = models.CharField(max_length=20, choices=Source.choices)
    expires_turn = models.PositiveIntegerField(null=True, blank=True)  # null = permanent
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.value} on {self.target} ({self.nation})"
