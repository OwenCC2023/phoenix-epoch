from django.db import models


class NationResourcePool(models.Model):
    """Aggregated national resource pool, updated each turn."""

    nation = models.OneToOneField("nations.Nation", on_delete=models.CASCADE, related_name="resource_pool")
    food = models.FloatField(default=0)
    materials = models.FloatField(default=0)
    energy = models.FloatField(default=0)
    kapital = models.FloatField(default=0)
    manpower = models.FloatField(default=0)
    research = models.FloatField(default=0)
    stability = models.FloatField(default=50.0)
    happiness = models.FloatField(default=50.0)
    literacy = models.FloatField(default=0.20)  # national average literacy (0.0-1.0)
    total_population = models.PositiveIntegerField(default=0)
    consecutive_food_deficit_turns = models.PositiveIntegerField(default=0)

    # Wealth & Taxation System — government balance of food-equivalent tokens.
    # May go negative (debt); interest compounds when negative (see taxation.py).
    treasury = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f"Resources for {self.nation}"


class ResourceLedger(models.Model):
    """Immutable per-turn record of national economy. Full audit trail."""

    nation = models.ForeignKey("nations.Nation", on_delete=models.CASCADE, related_name="ledger_entries")
    turn_number = models.PositiveIntegerField()
    province_production_total = models.JSONField(default=dict)
    integration_losses = models.JSONField(default=dict)
    national_modifier_effects = models.JSONField(default=dict)
    trade_net = models.JSONField(default=dict)
    consumption = models.JSONField(default=dict)
    final_pools = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("nation", "turn_number")
        ordering = ["-turn_number"]


class ControlPoolSnapshot(models.Model):
    """Per-turn snapshot of what control retains at province or region level.

    Informational only — these pools do not interact with gameplay yet.
    Exactly one of province or region is set per row.

    Provinces in a region have their pools aggregated at the region level;
    provinces outside any region are tracked individually.
    """

    province = models.ForeignKey(
        "provinces.Province",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="control_snapshots",
    )
    region = models.ForeignKey(
        "provinces.Region",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="control_snapshots",
    )
    turn_number = models.PositiveIntegerField()

    # Total = what was produced before control was applied.
    # Retained = total × (1 − control/100) — stays at province/region level.
    tax_revenue_total = models.FloatField(default=0)
    tax_revenue_retained = models.FloatField(default=0)
    trade_capacity_total = models.FloatField(default=0)
    trade_capacity_retained = models.FloatField(default=0)
    bc_total = models.FloatField(default=0)
    bc_retained = models.FloatField(default=0)
    research_total = models.FloatField(default=0)
    research_retained = models.FloatField(default=0)

    class Meta:
        ordering = ["-turn_number"]

    def __str__(self):
        target = f"province {self.province_id}" if self.province_id else f"region {self.region_id}"
        return f"ControlPoolSnapshot({target}, turn {self.turn_number})"

    def __str__(self):
        return f"Ledger: {self.nation} Turn {self.turn_number}"


class ProvinceLedger(models.Model):
    """Immutable per-turn record per province."""

    province = models.ForeignKey("provinces.Province", on_delete=models.CASCADE, related_name="ledger_entries")
    turn_number = models.PositiveIntegerField()
    population = models.PositiveIntegerField()
    sector_allocations = models.JSONField(default=dict)
    raw_production = models.JSONField(default=dict)
    local_consumption = models.JSONField(default=dict)
    exported_to_nation = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("province", "turn_number")
        ordering = ["-turn_number"]

    def __str__(self):
        return f"Province Ledger: {self.province} Turn {self.turn_number}"


class NationGoodStock(models.Model):
    """Manufactured goods stock for a nation, updated each turn by building production."""

    nation = models.OneToOneField("nations.Nation", on_delete=models.CASCADE, related_name="good_stocks")
    consumer_goods = models.FloatField(default=0)
    arms = models.FloatField(default=0)
    fuel = models.FloatField(default=0)
    machinery = models.FloatField(default=0)
    chemicals = models.FloatField(default=0)
    medicine = models.FloatField(default=0)
    components = models.FloatField(default=0)
    heavy_equipment = models.FloatField(default=0)
    military_goods = models.FloatField(default=0)

    def __str__(self):
        return f"Good stocks for {self.nation}"


class NationMarketSnapshot(models.Model):
    """Immutable per-turn snapshot of a nation's market state.

    Used by the pricing module to compute next turn's base resource prices from
    the marginal-producer productivity of the previous turn, and by analytics
    to reconstruct the shortage_factor history.
    """

    nation = models.ForeignKey(
        "nations.Nation", on_delete=models.CASCADE, related_name="market_snapshots"
    )
    turn_number = models.PositiveIntegerField()

    # {good_key: food_equiv_price}
    prices = models.JSONField(default=dict)
    # {good_key: qty consumed/produced this turn}
    monthly_demand = models.JSONField(default=dict)
    monthly_supply = models.JSONField(default=dict)
    # {resource_key: min per-worker subsistence productivity across marginal provinces}
    prev_subsistence_productivity = models.JSONField(default=dict)
    # {good_key: shortage_factor [0.5, 3.0]}
    shortage_factors = models.JSONField(default=dict)

    class Meta:
        unique_together = ("nation", "turn_number")
        ordering = ["-turn_number"]
        indexes = [
            models.Index(fields=["nation", "-turn_number"]),
        ]

    def __str__(self):
        return f"Market snapshot: {self.nation} turn {self.turn_number}"


class ResearchUnlock(models.Model):
    """Tracks which building sectors a nation has unlocked to higher tiers via research spending."""

    nation = models.ForeignKey("nations.Nation", on_delete=models.CASCADE, related_name="research_unlocks")
    sector = models.CharField(max_length=50)           # building category key from BUILDING_TYPES
    tier = models.PositiveIntegerField(default=1)      # 1 = L3-L4 unlocked, 2 = L5-L6 unlocked
    unlocked_turn = models.PositiveIntegerField()

    class Meta:
        unique_together = ("nation", "sector")

    def __str__(self):
        return f"{self.nation} — {self.sector} tier {self.tier}"
