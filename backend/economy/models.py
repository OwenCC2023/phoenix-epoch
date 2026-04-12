from django.db import models


class NationResourcePool(models.Model):
    """Aggregated national resource pool, updated each turn."""

    nation = models.OneToOneField("nations.Nation", on_delete=models.CASCADE, related_name="resource_pool")
    food = models.FloatField(default=0)
    materials = models.FloatField(default=0)
    energy = models.FloatField(default=0)
    wealth = models.FloatField(default=0)
    manpower = models.FloatField(default=0)
    research = models.FloatField(default=0)
    stability = models.FloatField(default=50.0)
    happiness = models.FloatField(default=50.0)
    literacy = models.FloatField(default=0.20)  # national average literacy (0.0-1.0)
    total_population = models.PositiveIntegerField(default=0)
    consecutive_food_deficit_turns = models.PositiveIntegerField(default=0)

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
