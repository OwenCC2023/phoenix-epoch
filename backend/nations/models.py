from django.conf import settings
from django.db import models


class Nation(models.Model):
    game = models.ForeignKey("games.Game", on_delete=models.CASCADE, related_name="nations")
    # Nullable to support NPC nations created by rebellion independence outcomes.
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="nations",
    )
    is_npc = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # Five-component government system. Each field holds a key from the
    # corresponding GOV_* dict in nations.government_constants.
    gov_direction = models.CharField(max_length=30, default="none")
    gov_economic_category = models.CharField(max_length=30, default="subsistence")
    gov_structure = models.CharField(max_length=30, default="power_consensus")
    gov_power_origin = models.CharField(max_length=30, default="law_and_order")
    gov_power_type = models.CharField(max_length=30, default="council")
    ideology_traits = models.JSONField(
        default=dict,
        help_text='{"strong": "trait_key", "weak": ["trait_key", "trait_key"]}',
    )
    motto = models.CharField(max_length=200, blank=True)
    is_alive = models.BooleanField(default=True)
    # The province designated as this nation's administrative capital.
    # Null until explicitly set (GM or player action). The trade system
    # requires a capital to compute trade route lengths.
    # When a capital province is captured by another nation, this FK
    # still points at it — get_effective_capital() checks ownership.
    capital_province = models.ForeignKey(
        "provinces.Province",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="capital_of_nation",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("game", "player")

    def __str__(self):
        return f"{self.name} ({self.game})"

    def get_effective_capital(self):
        """Return the capital province if still owned by this nation, else None.

        A capital is "lost" when its nation FK no longer points at this nation
        (i.e. captured by an enemy). This drives trade route inactivation.
        """
        cap = self.capital_province
        if cap is None:
            return None
        if cap.nation_id != self.pk:
            return None
        return cap


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


class NationDPPool(models.Model):
    """
    Tracks unspent Development Points available for a nation to allocate.

    Nations receive DP_ANNUAL_GRANT points every DP_GRANT_INTERVAL turns.
    Players spend from this pool via the ALLOCATE_DP order (System 17).
    """

    nation = models.OneToOneField(Nation, on_delete=models.CASCADE, related_name="dp_pool")
    available_points = models.PositiveIntegerField(default=0)
    last_grant_turn = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nation.name} DP pool: {self.available_points} available"


class NationMilitaryDP(models.Model):
    """
    Military Development Points for a nation (stub — stored, no mechanics yet).

    Military DP categories: strategy, tactics, logistics.
    Future systems (Doctrine, Combat) will consume these values.
    """

    nation = models.ForeignKey(Nation, on_delete=models.CASCADE, related_name="military_dp")
    category = models.CharField(max_length=20)  # strategy / tactics / logistics
    points = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("nation", "category")

    def __str__(self):
        return f"{self.nation.name} military DP – {self.category}: {self.points}"
