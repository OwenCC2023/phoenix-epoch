"""
Trade system models.

TradeRoute       — a persistent, directional, single-good trade route.
CapitalRelocation — tracks an in-progress capital move (peacetime 12-turn delay).
"""

from django.db import models


class TradeRoute(models.Model):
    """A directional trade route flowing one good from exporter to importer."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        PENDING = "pending", "Pending"                  # newly created, first turn not yet run
        INACTIVE_WAR = "inactive_war", "Inactive (War)" # capital lost / no path
        BROKEN_PATH = "broken_path", "Broken Path"      # pathfinder found no route

    class DomainMode(models.TextChoices):
        MULTI = "multi", "Multi-Domain"
        LAND = "land", "Land Only"
        SEA = "sea", "Sea Only"
        AIR = "air", "Air Only"

    game = models.ForeignKey(
        "games.Game", on_delete=models.CASCADE, related_name="trade_routes"
    )
    from_nation = models.ForeignKey(
        "nations.Nation", on_delete=models.CASCADE, related_name="outgoing_trade_routes"
    )
    to_nation = models.ForeignKey(
        "nations.Nation", on_delete=models.CASCADE, related_name="incoming_trade_routes"
    )

    good = models.CharField(max_length=50)
    quantity_per_turn = models.PositiveIntegerField()
    domain_mode = models.CharField(
        max_length=10, choices=DomainMode.choices, default=DomainMode.MULTI
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    # Pathfinder output — recalculated each turn when capitals move or zones change
    path_nodes = models.JSONField(default=list)       # list of [type, id] pairs
    total_length = models.FloatField(default=0.0)
    capacity_by_domain = models.JSONField(default=dict)  # {"land": X, "sea": Y, "air": Z}

    # Transit — goods spend arrival_turns in flight before being delivered
    arrival_turns = models.PositiveIntegerField(default=1)
    # in_flight: list of {"quantity": int, "arrives_turn": int}
    in_flight = models.JSONField(default=list)

    created_turn = models.PositiveIntegerField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return (
            f"{self.from_nation.name} → {self.to_nation.name}: "
            f"{self.quantity_per_turn}× {self.good} ({self.status})"
        )


class CapitalRelocation(models.Model):
    """Tracks a pending capital move initiated by a player order.

    One row per nation — enforced by OneToOneField.
    Completed rows are deleted after the nation's capital_province is updated.
    """

    nation = models.OneToOneField(
        "nations.Nation",
        on_delete=models.CASCADE,
        related_name="capital_relocation",
    )
    target_province = models.ForeignKey(
        "provinces.Province",
        on_delete=models.CASCADE,
        related_name="capital_relocations_targeting",
    )
    started_turn = models.PositiveIntegerField()
    completes_turn = models.PositiveIntegerField()
    # JSON snapshot of resources spent: {"wealth": 500, "materials": 200}
    cost_paid = models.JSONField(default=dict)

    def __str__(self):
        return (
            f"{self.nation.name} → capital to {self.target_province.name} "
            f"(completes turn {self.completes_turn})"
        )
