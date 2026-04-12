from django.db import models


class Turn(models.Model):
    """Represents a single turn in a game."""

    class Status(models.TextChoices):
        PENDING = "pending"
        PROCESSING = "processing"
        COMPLETED = "completed"
        FAILED = "failed"

    game = models.ForeignKey("games.Game", on_delete=models.CASCADE, related_name="turns")
    turn_number = models.PositiveIntegerField()
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    deadline = models.DateTimeField()
    resolution_log = models.JSONField(default=dict, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("game", "turn_number")
        ordering = ["-turn_number"]

    def __str__(self):
        return f"Turn {self.turn_number} ({self.game})"


class Order(models.Model):
    """A player's order for a given turn."""

    class OrderType(models.TextChoices):
        SET_ALLOCATION = "set_allocation"
        TRADE_OFFER = "trade_offer"
        TRADE_RESPONSE = "trade_response"
        POLICY_CHANGE = "policy_change"
        BUILD_IMPROVEMENT = "build_improvement"
        TRAIN_UNIT = "train_unit"
        CREATE_FORMATION = "create_formation"
        ASSIGN_TO_FORMATION = "assign_to_formation"
        RENAME_FORMATION = "rename_formation"
        CREATE_GROUP = "create_group"
        RENAME_GROUP = "rename_group"
        ASSIGN_FORMATION_TO_GROUP = "assign_formation_to_group"
        ESPIONAGE_ACTION = "espionage_action"
        SPECIALIZE_BRANCH_OFFICE = "specialize_branch_office"
        RESEARCH_UNLOCK = "research_unlock"
        ACQUIRE_PROVINCE = "acquire_province"

    class Status(models.TextChoices):
        DRAFT = "draft"
        SUBMITTED = "submitted"
        VALIDATED = "validated"
        EXECUTED = "executed"
        FAILED = "failed"

    turn = models.ForeignKey(Turn, on_delete=models.CASCADE, related_name="orders")
    nation = models.ForeignKey("nations.Nation", on_delete=models.CASCADE, related_name="orders")
    order_type = models.CharField(max_length=30, choices=OrderType.choices)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT)
    payload = models.JSONField(default=dict)
    validation_errors = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_type} by {self.nation} (Turn {self.turn.turn_number})"


class TurnSubmission(models.Model):
    """Tracks whether a player has submitted their orders for a turn."""

    turn = models.ForeignKey(Turn, on_delete=models.CASCADE, related_name="submissions")
    nation = models.ForeignKey("nations.Nation", on_delete=models.CASCADE, related_name="submissions")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("turn", "nation")

    def __str__(self):
        return f"{self.nation} submitted Turn {self.turn.turn_number}"
