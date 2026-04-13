import random

from django.db import models

from .constants import (
    TERRAIN_TYPES, TERRAIN_BASE_POPULATION, DEFAULT_PROVINCE_POPULATION,
    RELIEF_TYPES, VEGETATION_LEVELS, TEMPERATURE_BANDS,
    RELIEF_POP_MODIFIER, VEGETATION_POP_MODIFIER, TEMPERATURE_POP_MODIFIER,
)


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


def randomise_starting_population(
    terrain_type: str,
    relief: str = "flat",
    vegetation_level: str = "medium",
    temperature_band: str = "mild",
) -> int:
    """Return a randomised starting population for a new province.

    Centred on the terrain baseline modified by relief, vegetation, and
    temperature, then randomised ±30 %, rounded to the nearest 100.

    The three new axes were introduced with the trade system. Defaults
    preserve backward compatibility for callers that only pass terrain_type.

    Combined formula:
        base = TERRAIN_BASE_POPULATION[terrain]
               × RELIEF_POP_MODIFIER[relief]
               × VEGETATION_POP_MODIFIER[vegetation]
               × TEMPERATURE_POP_MODIFIER[temperature]
        result ∈ [base × 0.70, base × 1.30], rounded to nearest 100
    """
    base = TERRAIN_BASE_POPULATION.get(terrain_type, DEFAULT_PROVINCE_POPULATION)
    base = base * RELIEF_POP_MODIFIER.get(relief, 1.0)
    base = base * VEGETATION_POP_MODIFIER.get(vegetation_level, 1.0)
    base = base * TEMPERATURE_POP_MODIFIER.get(temperature_band, 1.0)
    low = int(base * 0.70)
    high = int(base * 1.30)
    raw = random.randint(low, high)
    return max(100, round(raw / 100) * 100)


class Region(models.Model):
    """Logical grouping of provinces within a nation for shared control settings.

    Provinces are not required to be geographically contiguous. When a region's
    control is set, all member provinces inherit that control value.
    """

    nation = models.ForeignKey(
        "nations.Nation", on_delete=models.CASCADE, related_name="regions"
    )
    name = models.CharField(max_length=100)
    control = models.FloatField(default=100.0)  # 1.0–100.0 percentage
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("nation", "name")

    def __str__(self):
        return f"{self.name} ({self.nation.name})"


class Province(models.Model):
    """The fundamental economic unit."""

    TERRAIN_CHOICES = [(key, val["label"]) for key, val in TERRAIN_TYPES.items()]
    RELIEF_CHOICES = [(key, val["label"]) for key, val in RELIEF_TYPES.items()]
    VEGETATION_CHOICES = [(key, val["label"]) for key, val in VEGETATION_LEVELS.items()]
    TEMPERATURE_CHOICES = [(key, val["label"]) for key, val in TEMPERATURE_BANDS.items()]

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
    # Trade friction environment (independent of biome terrain_type).
    # Seeded from terrain_type by data migration 0008; mappers can tune independently.
    relief = models.CharField(max_length=20, choices=RELIEF_CHOICES, default="flat")
    vegetation_level = models.CharField(max_length=20, choices=VEGETATION_CHOICES, default="low")
    temperature_band = models.CharField(max_length=20, choices=TEMPERATURE_CHOICES, default="mild")
    population = models.PositiveIntegerField(default=DEFAULT_PROVINCE_POPULATION)
    local_stability = models.FloatField(default=70.0)  # 0-100
    local_security = models.FloatField(default=30.0)   # 0-100
    local_happiness = models.FloatField(default=50.0)  # 0-100
    literacy = models.FloatField(default=0.20)         # 0.0-1.0, fraction of literate population
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

    # ---------------------------------------------------------------------------
    # Provincial Integration System
    # ---------------------------------------------------------------------------

    # Province-level ideology traits. Core provinces mirror the national ideology.
    # Non-core provinces start with their own traits and normalize over time.
    # Format: {"strong": "trait_key", "weak": ["trait1", "trait2"]}
    ideology_traits = models.JSONField(default=dict, blank=True)

    # The nation that originally owned this province (for reconquest mechanics).
    original_nation = models.ForeignKey(
        "nations.Nation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="original_provinces",
    )

    # Core provinces behave identically to the rest of the nation.
    # Non-core provinces apply stability/happiness penalties during normalization.
    is_core = models.BooleanField(default=True)

    # Normalization tracks when a non-core province started integrating and
    # how long the full normalization period lasts (in turns).
    normalization_started_turn = models.PositiveIntegerField(null=True, blank=True)
    normalization_duration = models.PositiveIntegerField(null=True, blank=True)

    # De-integration tracks ideology fade when a province leaves a nation.
    # Separate from normalization fields — a province could be re-acquired
    # mid-deintegration, requiring both state machines to run independently.
    deintegration_started_turn = models.PositiveIntegerField(null=True, blank=True)
    deintegration_duration = models.PositiveIntegerField(null=True, blank=True)

    # Control System — how tightly the nation governs this province (1–100%).
    # Effective control uses region.control if province is in a region.
    control = models.FloatField(default=100.0)
    region = models.ForeignKey(
        "provinces.Region",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="provinces",
    )

    # Rebellion state — set when a rebel formation spawns in this province.
    # The timer counts down until either the nation suppresses the rebellion
    # (via combat) or the rebels accomplish their objective.
    is_rebel_occupied = models.BooleanField(default=False)
    rebel_timer_start_turn = models.PositiveIntegerField(null=True, blank=True)
    rebel_timer_duration = models.PositiveIntegerField(null=True, blank=True)

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
