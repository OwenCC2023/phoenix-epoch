import random

from django.db import models

from .constants import TERRAIN_TYPES, TERRAIN_BASE_POPULATION, DEFAULT_PROVINCE_POPULATION


class AirZone(models.Model):
    game = models.ForeignKey("games.Game", on_delete=models.CASCADE, related_name="air_zones")
    name = models.CharField(max_length=100)
    adjacent_air_zones = models.ManyToManyField(
        "self", symmetrical=True, blank=True, db_table="provinces_airzone_adjacency"
    )

    def __str__(self):
        return f"{self.name} (Air, game {self.game_id})"


class SeaZone(models.Model):
    game = models.ForeignKey("games.Game", on_delete=models.CASCADE, related_name="sea_zones")
    name = models.CharField(max_length=100)
    adjacent_sea_zones = models.ManyToManyField(
        "self", symmetrical=True, blank=True, db_table="provinces_seazone_adjacency"
    )
    adjacent_air_zones = models.ManyToManyField(
        AirZone, blank=True, related_name="adjacent_sea_zones", db_table="provinces_seazone_airzone"
    )

    def __str__(self):
        return f"{self.name} (Sea, game {self.game_id})"


class RiverZone(models.Model):
    game = models.ForeignKey("games.Game", on_delete=models.CASCADE, related_name="river_zones")
    name = models.CharField(max_length=100)
    sea_zone = models.ForeignKey(
        SeaZone, on_delete=models.SET_NULL, null=True, blank=True, related_name="river_zones"
    )
    adjacent_river_zones = models.ManyToManyField(
        "self", symmetrical=True, blank=True, db_table="provinces_riverzone_adjacency"
    )
    adjacent_air_zones = models.ManyToManyField(
        AirZone, blank=True, related_name="adjacent_river_zones", db_table="provinces_riverzone_airzone"
    )

    def __str__(self):
        return f"{self.name} (River, game {self.game_id})"


def randomise_starting_population(terrain_type: str) -> int:
    """Return a randomised starting population for a new province.

    Centred on the terrain baseline, ±30 %, rounded to the nearest 100.
    Call this explicitly when creating a Province rather than relying on
    field default, because the terrain type is needed to pick the baseline.
    """
    base = TERRAIN_BASE_POPULATION.get(terrain_type, DEFAULT_PROVINCE_POPULATION)
    low = int(base * 0.70)
    high = int(base * 1.30)
    raw = random.randint(low, high)
    return max(100, round(raw / 100) * 100)


class Province(models.Model):
    """The fundamental economic unit."""

    TERRAIN_CHOICES = [(key, val["label"]) for key, val in TERRAIN_TYPES.items()]

    DESIGNATION_CHOICES = [
        ("rural", "Rural"),
        ("urban", "Urban"),
        ("post_urban", "Post-Urban"),
        ("capital", "Capital"),
    ]

    game = models.ForeignKey("games.Game", on_delete=models.CASCADE, related_name="provinces")
    nation = models.ForeignKey(
        "nations.Nation", on_delete=models.SET_NULL, null=True, blank=True, related_name="provinces"
    )
    name = models.CharField(max_length=100)
    terrain_type = models.CharField(max_length=20, choices=TERRAIN_CHOICES)
    population = models.PositiveIntegerField(default=DEFAULT_PROVINCE_POPULATION)
    local_stability = models.FloatField(default=70.0)  # 0-100
    local_security = models.FloatField(default=30.0)   # 0-100
    designation = models.CharField(max_length=20, choices=DESIGNATION_CHOICES, default="rural")
    is_capital = models.BooleanField(default=False)
    is_coastal = models.BooleanField(default=False)   # can build Naval Base
    is_river = models.BooleanField(default=False)     # can build Naval Base

    # Map coordinates (set when map is developed; travel time uses these when non-null)
    center_x = models.FloatField(null=True, blank=True)
    center_y = models.FloatField(null=True, blank=True)
    # Distance from province center to the border edge facing coastal/river zones (map units).
    # Used for province<->sea and province<->river cross-type transition times.
    # Null until map is developed; formula falls back to BASE_EMBARK_TIME when null.
    sea_border_distance = models.FloatField(null=True, blank=True)
    river_border_distance = models.FloatField(null=True, blank=True)

    # Zone assignment and adjacency
    air_zone = models.ForeignKey(
        AirZone, on_delete=models.SET_NULL, null=True, blank=True, related_name="provinces"
    )
    adjacent_provinces = models.ManyToManyField(
        "self", symmetrical=True, blank=True, db_table="provinces_province_adjacency"
    )
    adjacent_sea_zones = models.ManyToManyField(
        SeaZone, blank=True, related_name="adjacent_provinces", db_table="provinces_province_seazone"
    )
    adjacent_river_zones = models.ManyToManyField(
        RiverZone, blank=True, related_name="adjacent_provinces", db_table="provinces_province_riverzone"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        owner = self.nation.name if self.nation else "Unowned"
        return f"{self.name} ({owner})"


class ProvinceResources(models.Model):
    """Current resource output of a province (recalculated each turn)."""

    province = models.OneToOneField(Province, on_delete=models.CASCADE, related_name="resources")
    food = models.FloatField(default=0)
    materials = models.FloatField(default=0)
    energy = models.FloatField(default=0)
    wealth = models.FloatField(default=0)
    manpower = models.FloatField(default=0)
    research = models.FloatField(default=0)
    updated_turn = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Province resources"

    def __str__(self):
        return f"Resources for {self.province}"


class ProvinceSectorAllocation(models.Model):
    """How a province's population is distributed across sectors."""

    SECTOR_CHOICES = [
        ("agriculture", "Agriculture"),
        ("industry", "Industry"),
        ("energy", "Energy"),
        ("commerce", "Commerce"),
        ("military", "Military"),
        ("research", "Research"),
    ]

    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="sector_allocations")
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES)
    percentage = models.PositiveIntegerField()
    turn_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ("province", "sector", "turn_number")

    def __str__(self):
        return f"{self.province} - {self.sector}: {self.percentage}%"


class Building(models.Model):
    """A building in a province, part of the economic production chain."""

    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="buildings")
    building_type = models.CharField(max_length=50)  # key from BUILDING_TYPES
    level = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)  # player can toggle on/off
    under_construction = models.BooleanField(default=False)
    construction_turns_remaining = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("province", "building_type")

    def __str__(self):
        return f"{self.building_type} (Lvl {self.level}) in {self.province}"


# ---------------------------------------------------------------------------
# Military models
# ---------------------------------------------------------------------------

class MilitaryGroup(models.Model):
    """
    Domain-agnostic command structure for organising formations into fronts.
    Has no fixed province location — pure command hierarchy for the future
    combat system.
    """

    nation = models.ForeignKey(
        "nations.Nation", on_delete=models.CASCADE, related_name="military_groups"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.nation.name})"


class Formation(models.Model):
    """
    A domain-specific grouping of military units located in a province.

    Two types:
      - reserve  : auto-created when the first unit of a domain is trained in a
                   province that has no existing reserve formation for that domain.
                   Named automatically; player can rename.
      - active   : player-created; can be placed in any province; can be assigned
                   to a MilitaryGroup for command structure.

    One reserve formation per (nation, province, domain) — enforced by a
    partial unique constraint.
    """

    class Domain(models.TextChoices):
        ARMY = "army", "Army"
        NAVY = "navy", "Navy"
        AIR = "air", "Air"

    class FormationType(models.TextChoices):
        RESERVE = "reserve", "Reserve"
        ACTIVE = "active", "Active"

    nation = models.ForeignKey(
        "nations.Nation", on_delete=models.CASCADE, related_name="formations"
    )
    group = models.ForeignKey(
        MilitaryGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="formations",
    )
    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="formations",
    )
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=10, choices=Domain.choices)
    formation_type = models.CharField(
        max_length=10, choices=FormationType.choices, default=FormationType.RESERVE
    )
    # Recomputed and stored each turn (end of simulation).
    # Can exceed sum(unit.quantity) — future traits / morale boosts may push it
    # above quantity; supply deficits push it below.
    effective_strength = models.FloatField(default=0.0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["nation", "province", "domain"],
                condition=models.Q(formation_type="reserve"),
                name="unique_reserve_formation_per_domain_province_nation",
            )
        ]

    def __str__(self):
        return f"{self.name} [{self.domain}] ({self.nation.name})"


class MilitaryUnit(models.Model):
    """
    A stack of units of a single type within a Formation.

    quantity            — active, ready units (integer; becomes fractional
                          post-combat losses via the future combat system).
    quantity_in_training— units currently being trained at training_province.
    construction_turns_remaining — FloatField so synergy/trait speed bonuses
                          accumulate as fractional ticks each turn.
    is_active           — False when manufactured-goods/fuel upkeep is unmet.
    quantity_in_transit — scaffold: units that have finished training but
                          have not yet reached the formation's province.
    transit_turns_remaining — scaffold: turns until in-transit units arrive.
    training_province   — province where the training base is located.
    """

    formation = models.ForeignKey(
        Formation, on_delete=models.CASCADE, related_name="units"
    )
    unit_type = models.CharField(max_length=30)   # key from UNIT_TYPES
    quantity = models.PositiveIntegerField(default=0)
    quantity_in_training = models.PositiveIntegerField(default=0)
    construction_turns_remaining = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)

    # Transit scaffold — movement to formation location (future combat system)
    quantity_in_transit = models.PositiveIntegerField(default=0)
    transit_turns_remaining = models.FloatField(default=0.0)

    # Province where training is taking place (where the base is)
    training_province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="units_in_training",
    )

    class Meta:
        unique_together = ("formation", "unit_type")

    def __str__(self):
        return f"{self.quantity}× {self.unit_type} in {self.formation}"
