"""Espionage system models.

EspionageState   — per attacker-target nation pair, stores computed attack/defense/transparency
EspionageAction  — tracks active espionage operations (foreign and domestic)
IntelligenceSharing — voluntary per-nation-per-category info sharing toggles
BranchOfficeSpecialization — links a branch_office Building to a foreign action type
"""

from django.db import models


class EspionageState(models.Model):
    """Computed espionage values per attacker-target pair, updated each turn."""

    game = models.ForeignKey(
        "games.Game", on_delete=models.CASCADE, related_name="espionage_states"
    )
    attacker = models.ForeignKey(
        "nations.Nation", on_delete=models.CASCADE, related_name="espionage_attacks"
    )
    target = models.ForeignKey(
        "nations.Nation", on_delete=models.CASCADE, related_name="espionage_defenses"
    )

    # Computed values (updated each turn)
    national_attack = models.FloatField(default=0.0)
    national_defense = models.FloatField(default=0.0)
    transparency = models.FloatField(default=0.0)  # 0.0–1.0

    # Structured revelation snapshot (regenerated each turn)
    revealed_info = models.JSONField(default=dict)

    turn_updated = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("game", "attacker", "target")

    def __str__(self):
        return f"Espionage: {self.attacker} → {self.target} (T={self.transparency:.0%})"


class EspionageAction(models.Model):
    """An active or completed espionage operation."""

    class ActionType(models.TextChoices):
        # Foreign actions
        INVESTIGATE_PROVINCE = "investigate_province"
        PROMOTE_FOREIGN_IDEOLOGY = "promote_foreign_ideology"
        TERRORIST_ATTACK = "terrorist_attack"
        SABOTAGE_BUILDING = "sabotage_building"
        PERSUADE_TO_JOIN = "persuade_to_join"
        # Domestic actions
        SUPPRESS_FOREIGN_OPERATIONS = "suppress_foreign_operations"

    class Status(models.TextChoices):
        ACTIVE = "active"
        COMPLETED = "completed"
        FAILED = "failed"
        CANCELLED = "cancelled"

    game = models.ForeignKey("games.Game", on_delete=models.CASCADE)
    nation = models.ForeignKey(
        "nations.Nation", on_delete=models.CASCADE, related_name="espionage_actions"
    )
    action_type = models.CharField(max_length=40, choices=ActionType.choices)
    target_nation = models.ForeignKey(
        "nations.Nation",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="espionage_actions_against",
    )
    target_province = models.ForeignKey(
        "provinces.Province", on_delete=models.CASCADE, null=True, blank=True
    )
    target_building_type = models.CharField(max_length=60, blank=True, default="")
    payload = models.JSONField(default=dict)
    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.ACTIVE
    )
    started_turn = models.PositiveIntegerField()
    expires_turn = models.PositiveIntegerField(null=True, blank=True)
    result = models.JSONField(default=dict)

    class Meta:
        indexes = [
            models.Index(fields=["game", "nation", "status"]),
        ]

    def __str__(self):
        target = self.target_nation or "domestic"
        return f"{self.nation} {self.action_type} → {target} ({self.status})"


class IntelligenceSharing(models.Model):
    """Voluntary information sharing toggle per source-viewer-category."""

    class Category(models.TextChoices):
        BUILDING_LOCATIONS = "building_locations"
        PROVINCE_LEVEL_INFO = "province_level_info"
        POSITIONS_OF_FORMATIONS = "positions_of_formations"
        COINTEL = "cointel"
        FOREIGN_ESPIONAGE = "foreign_espionage"

    game = models.ForeignKey("games.Game", on_delete=models.CASCADE)
    source_nation = models.ForeignKey(
        "nations.Nation",
        on_delete=models.CASCADE,
        related_name="intelligence_shared_out",
    )
    viewer_nation = models.ForeignKey(
        "nations.Nation",
        on_delete=models.CASCADE,
        related_name="intelligence_shared_in",
    )
    category = models.CharField(max_length=30, choices=Category.choices)
    is_shared = models.BooleanField(default=False)

    class Meta:
        unique_together = ("game", "source_nation", "viewer_nation", "category")

    def __str__(self):
        state = "shared" if self.is_shared else "hidden"
        return f"{self.source_nation} → {self.viewer_nation}: {self.category} ({state})"


class BranchOfficeSpecialization(models.Model):
    """Links a branch_office Building to a specific foreign action type.

    Created via a separate 'specialize_branch_office' order after construction.
    """

    building = models.OneToOneField(
        "provinces.Building",
        on_delete=models.CASCADE,
        related_name="espionage_specialization",
    )
    action_type = models.CharField(max_length=40)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    action_type__in=[
                        "investigate_province",
                        "promote_foreign_ideology",
                        "terrorist_attack",
                        "sabotage_building",
                    ]
                ),
                name="branch_office_valid_specialization",
            )
        ]

    def __str__(self):
        return f"Branch office #{self.building_id} → {self.action_type}"
