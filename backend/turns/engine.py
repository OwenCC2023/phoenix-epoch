"""Turn resolution engine — orchestrates the full turn lifecycle."""
import logging
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .models import Turn, Order, TurnSubmission
from .validators import validate_order

logger = logging.getLogger(__name__)


class TurnResolutionEngine:
    """Orchestrates turn resolution for a game."""

    def __init__(self, game):
        self.game = game
        self.log = []

    @transaction.atomic
    def resolve_current_turn(self):
        """Resolve the current pending turn."""
        turn = (
            Turn.objects.select_for_update()
            .filter(game=self.game, status=Turn.Status.PENDING)
            .order_by("-turn_number")
            .first()
        )

        if not turn:
            self._log("No pending turn to resolve")
            return None

        turn.status = Turn.Status.PROCESSING
        turn.save(update_fields=["status"])
        self._log(f"Processing Turn {turn.turn_number}")

        try:
            # Step 1: Validate all submitted orders
            self._validate_orders(turn)

            # Step 2: Apply defaults for non-submitting nations
            self._apply_defaults(turn)

            # Step 3: Execute orders in priority order
            self._execute_policy_changes(turn)
            self._execute_allocations(turn)
            self._execute_build_orders(turn)
            self._execute_trades(turn)
            self._execute_military_orders(turn)

            # Step 4: Run economy simulation
            self._run_economy_simulation(turn)

            # Step 5: Check collapse conditions
            self._check_collapse_conditions(turn)

            # Step 6: Complete turn and create next
            turn.status = Turn.Status.COMPLETED
            turn.resolved_at = timezone.now()
            turn.resolution_log = {"events": self.log}
            turn.save()

            next_turn = self._create_next_turn(turn)
            self._log(f"Turn {turn.turn_number} resolved. Next turn: {next_turn.turn_number}")

            # Update game state
            self.game.current_turn_number = next_turn.turn_number
            self.game.current_turn_deadline = next_turn.deadline
            self.game.save(update_fields=["current_turn_number", "current_turn_deadline"])

            return turn

        except Exception as e:
            logger.exception(f"Turn resolution failed for game {self.game.id}")
            turn.status = Turn.Status.FAILED
            turn.resolution_log = {"events": self.log, "error": str(e)}
            turn.save()
            raise

    def _validate_orders(self, turn):
        """Validate all submitted orders."""
        orders = Order.objects.filter(turn=turn, status=Order.Status.SUBMITTED)
        for order in orders:
            errors = validate_order(order)
            if errors:
                order.status = Order.Status.FAILED
                order.validation_errors = errors
                self._log(f"Order {order.id} ({order.order_type}) failed validation: {errors}")
            else:
                order.status = Order.Status.VALIDATED
            order.save(update_fields=["status", "validation_errors"])

    def _apply_defaults(self, turn):
        """For nations that didn't submit orders, keep previous allocations."""
        from nations.models import Nation

        submitted_nation_ids = set(
            TurnSubmission.objects.filter(turn=turn).values_list("nation_id", flat=True)
        )
        all_nations = Nation.objects.filter(game=self.game, is_alive=True)

        for nation in all_nations:
            if nation.id not in submitted_nation_ids:
                self._log(f"{nation.name} did not submit orders — using defaults")

    def _execute_policy_changes(self, turn):
        """Execute policy change orders (government or policy level changes)."""
        from nations.helpers import apply_government_modifiers
        from nations.models import NationPolicy
        from nations.policy_constants import POLICY_CATEGORIES

        orders = Order.objects.filter(
            turn=turn,
            order_type=Order.OrderType.POLICY_CHANGE,
            status=Order.Status.VALIDATED,
        )
        for order in orders:
            payload = order.payload
            nation = order.nation
            if payload["change_type"] == "government":
                component = payload["component"]   # e.g. "direction"
                field = f"gov_{component}"         # e.g. "gov_direction"
                new_value = payload["new_value"]
                setattr(nation, field, new_value)
                nation.save(update_fields=[field])
                apply_government_modifiers(nation)
                self._log(f"{nation.name} changed gov_{component} to {new_value}")
                # Sweep policies: force any newly-disabled ones to default
                self._sweep_disabled_policies(nation, turn)
            elif payload["change_type"] == "policy_level":
                category = payload["category"]
                new_level = payload["new_level"]
                policy, created = NationPolicy.objects.get_or_create(
                    nation=nation,
                    category=category,
                    defaults={"level": new_level, "changed_turn": turn.turn_number},
                )
                if not created:
                    policy.level = new_level
                    policy.changed_turn = turn.turn_number
                    policy.save(update_fields=["level", "changed_turn"])
                cat_def = POLICY_CATEGORIES.get(category, {})
                levels = cat_def.get("levels", [])
                level_name = levels[new_level]["name"] if new_level < len(levels) else str(new_level)
                self._log(f"{nation.name} changed {category} to {level_name}")
            order.status = Order.Status.EXECUTED
            order.save(update_fields=["status"])

    def _sweep_disabled_policies(self, nation, turn):
        """
        After a gov change, force any newly-disabled policies to default level.

        Checks GOV_POLICY_DISABLES for each of the nation's current gov options.
        If a NationPolicy row matches a disabled (category, level), reset it to
        the category's default_level.
        """
        from nations.models import NationPolicy
        from nations.policy_constants import POLICY_CATEGORIES
        from nations.disabling_rules import GOV_POLICY_DISABLES

        gov_values = [
            nation.gov_direction,
            nation.gov_economic_category,
            nation.gov_structure,
            nation.gov_power_origin,
            nation.gov_power_type,
        ]

        # Collect all disabled (cat, level) pairs from current gov options
        disabled_set = set()
        for gov_val in gov_values:
            for pair in GOV_POLICY_DISABLES.get(gov_val, []):
                disabled_set.add(pair)

        if not disabled_set:
            return

        # Check each policy row
        for policy in NationPolicy.objects.filter(nation=nation):
            if (policy.category, policy.level) in disabled_set:
                cat_def = POLICY_CATEGORIES.get(policy.category, {})
                default = cat_def.get("default_level", 0)
                old_level = policy.level
                policy.level = default
                policy.changed_turn = turn.turn_number
                policy.save(update_fields=["level", "changed_turn"])
                self._log(
                    f"{nation.name}: {policy.category} forced from "
                    f"level {old_level} to default {default} (gov disabling)"
                )

    def _execute_allocations(self, turn):
        """Execute sector allocation orders."""
        from provinces.models import ProvinceSectorAllocation

        orders = Order.objects.filter(
            turn=turn,
            order_type=Order.OrderType.SET_ALLOCATION,
            status=Order.Status.VALIDATED,
        )
        for order in orders:
            payload = order.payload
            for alloc in payload["allocations"]:
                ProvinceSectorAllocation.objects.update_or_create(
                    province_id=payload["province_id"],
                    sector=alloc["sector"],
                    turn_number=turn.turn_number,
                    defaults={"percentage": alloc["percentage"]},
                )
            order.status = Order.Status.EXECUTED
            order.save(update_fields=["status"])
            self._log(f"{order.nation.name} set allocations for province {payload['province_id']}")

    def _execute_build_orders(self, turn):
        """Execute build improvement orders."""
        from provinces.constants import IMPROVEMENT_TYPES
        from provinces.models import ProvinceImprovement

        orders = Order.objects.filter(
            turn=turn,
            order_type=Order.OrderType.BUILD_IMPROVEMENT,
            status=Order.Status.VALIDATED,
        )
        for order in orders:
            payload = order.payload
            imp_type = payload["improvement_type"]
            imp_def = IMPROVEMENT_TYPES[imp_type]

            existing = ProvinceImprovement.objects.filter(
                province_id=payload["province_id"],
                improvement_type=imp_type,
            ).first()

            if existing:
                existing.under_construction = True
                existing.construction_turns_remaining = imp_def["build_turns"]
                existing.save()
            else:
                ProvinceImprovement.objects.create(
                    province_id=payload["province_id"],
                    improvement_type=imp_type,
                    level=0,
                    under_construction=True,
                    construction_turns_remaining=imp_def["build_turns"],
                )

            order.status = Order.Status.EXECUTED
            order.save(update_fields=["status"])
            self._log(f"{order.nation.name} started building {imp_type}")

        # Advance construction on all in-progress improvements
        from provinces.models import ProvinceImprovement as PI
        building = PI.objects.filter(
            province__game=self.game, under_construction=True
        )
        for imp in building:
            imp.construction_turns_remaining -= 1
            if imp.construction_turns_remaining <= 0:
                imp.under_construction = False
                imp.construction_turns_remaining = 0
                imp.level += 1
                self._log(f"Improvement {imp.improvement_type} completed in {imp.province.name} (now level {imp.level})")
            imp.save()

    def _execute_trades(self, turn):
        """Execute trade orders (offers and responses)."""
        from economy.models import TradeOffer, NationResourcePool

        # Process trade responses first
        responses = Order.objects.filter(
            turn=turn,
            order_type=Order.OrderType.TRADE_RESPONSE,
            status=Order.Status.VALIDATED,
        )
        for order in responses:
            payload = order.payload
            try:
                trade = TradeOffer.objects.get(pk=payload["trade_offer_id"])
            except TradeOffer.DoesNotExist:
                order.status = Order.Status.FAILED
                order.validation_errors = ["Trade offer not found"]
                order.save()
                continue

            if payload["action"] == "accept":
                # Transfer resources
                from_pool = NationResourcePool.objects.get(nation=trade.from_nation)
                to_pool = NationResourcePool.objects.get(nation=trade.to_nation)

                # Check sender can afford
                can_afford = True
                for resource, amount in trade.offering.items():
                    if getattr(from_pool, resource, 0) < amount:
                        can_afford = False
                        break

                if can_afford:
                    for resource, amount in trade.offering.items():
                        setattr(from_pool, resource, getattr(from_pool, resource) - amount)
                        setattr(to_pool, resource, getattr(to_pool, resource) + amount)
                    for resource, amount in trade.requesting.items():
                        setattr(to_pool, resource, getattr(to_pool, resource) - amount)
                        setattr(from_pool, resource, getattr(from_pool, resource) + amount)
                    from_pool.save()
                    to_pool.save()
                    trade.status = TradeOffer.Status.EXECUTED
                    self._log(f"Trade executed: {trade.from_nation.name} <-> {trade.to_nation.name}")
                else:
                    trade.status = TradeOffer.Status.EXPIRED
                    self._log(f"Trade failed (insufficient resources): {trade.from_nation.name}")
            else:
                trade.status = TradeOffer.Status.REJECTED
                self._log(f"Trade rejected by {trade.to_nation.name}")

            trade.save()
            order.status = Order.Status.EXECUTED
            order.save(update_fields=["status"])

        # Create new trade offers
        offers = Order.objects.filter(
            turn=turn,
            order_type=Order.OrderType.TRADE_OFFER,
            status=Order.Status.VALIDATED,
        )
        for order in offers:
            payload = order.payload
            TradeOffer.objects.create(
                game=self.game,
                from_nation=order.nation,
                to_nation_id=payload["to_nation_id"],
                turn_number=turn.turn_number,
                offering=payload.get("offering", {}),
                requesting=payload.get("requesting", {}),
            )
            order.status = Order.Status.EXECUTED
            order.save(update_fields=["status"])
            self._log(f"{order.nation.name} created trade offer")

    def _execute_military_orders(self, turn):
        """Execute all military orders: train_unit, create_formation, assign_to_formation,
        rename_formation, create_group, rename_group, assign_formation_to_group."""

        military_types = [
            Order.OrderType.TRAIN_UNIT,
            Order.OrderType.CREATE_FORMATION,
            Order.OrderType.ASSIGN_TO_FORMATION,
            Order.OrderType.RENAME_FORMATION,
            Order.OrderType.CREATE_GROUP,
            Order.OrderType.RENAME_GROUP,
            Order.OrderType.ASSIGN_FORMATION_TO_GROUP,
        ]
        orders = Order.objects.filter(
            turn=turn,
            order_type__in=military_types,
            status=Order.Status.VALIDATED,
        )
        for order in orders:
            try:
                if order.order_type == Order.OrderType.TRAIN_UNIT:
                    self._exec_train_unit(order, turn)
                elif order.order_type == Order.OrderType.CREATE_FORMATION:
                    self._exec_create_formation(order)
                elif order.order_type == Order.OrderType.ASSIGN_TO_FORMATION:
                    self._exec_assign_to_formation(order)
                elif order.order_type == Order.OrderType.RENAME_FORMATION:
                    self._exec_rename_formation(order)
                elif order.order_type == Order.OrderType.CREATE_GROUP:
                    self._exec_create_group(order)
                elif order.order_type == Order.OrderType.RENAME_GROUP:
                    self._exec_rename_group(order)
                elif order.order_type == Order.OrderType.ASSIGN_FORMATION_TO_GROUP:
                    self._exec_assign_formation_to_group(order)
                order.status = Order.Status.EXECUTED
                order.save(update_fields=["status"])
            except Exception as exc:
                order.status = Order.Status.FAILED
                order.validation_errors = [str(exc)]
                order.save(update_fields=["status", "validation_errors"])
                self._log(f"Military order {order.id} ({order.order_type}) failed: {exc}")

    def _exec_train_unit(self, order, turn):
        from provinces.military_constants import UNIT_TYPES, DOMAIN_TO_BASE
        from provinces.models import Province, Formation, MilitaryUnit
        from economy.models import NationGoodStock, NationResourcePool

        payload = order.payload
        province = Province.objects.get(pk=payload["province_id"])
        unit_type = payload["unit_type"]
        quantity = payload["quantity"]
        formation_id = payload.get("formation_id")

        unit_def = UNIT_TYPES[unit_type]
        domain = unit_def["domain"]

        # Deduct costs from nation pools
        pool = NationResourcePool.objects.get(nation=order.nation)
        good_stock = NationGoodStock.objects.get(nation=order.nation)
        good_stock.military_goods -= unit_def["military_goods_cost"] * quantity
        pool.manpower -= unit_def["manpower_cost"] * quantity
        good_stock.save(update_fields=["military_goods"])
        pool.save(update_fields=["manpower"])

        # Find or create the target formation
        if formation_id:
            formation = Formation.objects.get(pk=formation_id)
        else:
            # Use or create the reserve formation for this domain in this province
            formation_name = f"Reserve {province.name} {domain.capitalize()}"
            formation, _ = Formation.objects.get_or_create(
                nation=order.nation,
                province=province,
                domain=domain,
                formation_type=Formation.FormationType.RESERVE,
                defaults={"name": formation_name},
            )

        # Create or update the MilitaryUnit row for this formation + unit_type
        unit, created = MilitaryUnit.objects.get_or_create(
            formation=formation,
            unit_type=unit_type,
            defaults={
                "quantity": 0,
                "quantity_in_training": quantity,
                "construction_turns_remaining": float(unit_def["construction_turns"]),
                "training_province": province,
            },
        )
        if not created:
            if unit.quantity_in_training > 0:
                raise ValueError(
                    f"A {unit_type} unit is already in training for this formation"
                )
            unit.quantity_in_training = quantity
            unit.construction_turns_remaining = float(unit_def["construction_turns"])
            unit.training_province = province
            unit.save(update_fields=[
                "quantity_in_training", "construction_turns_remaining", "training_province"
            ])

        self._log(
            f"{order.nation.name} training {quantity}× {unit_type} in {province.name} "
            f"(formation: {formation.name})"
        )

    def _exec_create_formation(self, order):
        from provinces.models import Province, MilitaryGroup, Formation

        payload = order.payload
        province = Province.objects.get(pk=payload["province_id"])
        group = None
        if payload.get("group_id"):
            group = MilitaryGroup.objects.get(pk=payload["group_id"])

        formation = Formation.objects.create(
            nation=order.nation,
            province=province,
            name=payload["name"].strip(),
            domain=payload["domain"],
            formation_type=Formation.FormationType.ACTIVE,
            group=group,
        )
        self._log(f"{order.nation.name} created formation '{formation.name}' [{formation.domain}]")

    def _exec_assign_to_formation(self, order):
        from provinces.models import Formation, MilitaryUnit

        payload = order.payload
        unit_type = payload["unit_type"]
        quantity = payload["quantity"]
        source = Formation.objects.get(pk=payload["source_formation_id"])
        target = Formation.objects.get(pk=payload["target_formation_id"])

        # Deduct from source
        source_unit = MilitaryUnit.objects.get(formation=source, unit_type=unit_type)
        source_unit.quantity -= quantity
        source_unit.save(update_fields=["quantity"])

        # Add to target (create row if it does not exist)
        target_unit, _ = MilitaryUnit.objects.get_or_create(
            formation=target,
            unit_type=unit_type,
            defaults={"quantity": 0},
        )
        target_unit.quantity += quantity
        target_unit.save(update_fields=["quantity"])

        self._log(
            f"{order.nation.name} transferred {quantity}× {unit_type} "
            f"from '{source.name}' to '{target.name}'"
        )

    def _exec_rename_formation(self, order):
        from provinces.models import Formation

        payload = order.payload
        formation = Formation.objects.get(pk=payload["formation_id"])
        old_name = formation.name
        formation.name = payload["new_name"].strip()
        formation.save(update_fields=["name"])
        self._log(f"{order.nation.name} renamed formation '{old_name}' → '{formation.name}'")

    def _exec_create_group(self, order):
        from provinces.models import MilitaryGroup

        group = MilitaryGroup.objects.create(
            nation=order.nation,
            name=order.payload["name"].strip(),
        )
        self._log(f"{order.nation.name} created group '{group.name}'")

    def _exec_rename_group(self, order):
        from provinces.models import MilitaryGroup

        payload = order.payload
        group = MilitaryGroup.objects.get(pk=payload["group_id"])
        old_name = group.name
        group.name = payload["new_name"].strip()
        group.save(update_fields=["name"])
        self._log(f"{order.nation.name} renamed group '{old_name}' → '{group.name}'")

    def _exec_assign_formation_to_group(self, order):
        from provinces.models import Formation, MilitaryGroup

        payload = order.payload
        formation = Formation.objects.get(pk=payload["formation_id"])
        group_id = payload.get("group_id")
        formation.group = MilitaryGroup.objects.get(pk=group_id) if group_id else None
        formation.save(update_fields=["group"])
        group_name = formation.group.name if formation.group else "none"
        self._log(
            f"{order.nation.name} assigned formation '{formation.name}' to group '{group_name}'"
        )

    def _run_economy_simulation(self, turn):
        """Run the economy simulation engine."""
        from economy.simulation import simulate_economy_for_game

        self._log("Running economy simulation...")
        simulate_economy_for_game(self.game, turn.turn_number)
        self._log("Economy simulation complete")

    def _check_collapse_conditions(self, turn):
        """Check if any nations have collapsed."""
        from economy.constants import COLLAPSE_STARVATION_TURNS
        from economy.models import NationResourcePool
        from nations.models import Nation

        nations = Nation.objects.filter(game=self.game, is_alive=True)
        for nation in nations:
            try:
                pool = NationResourcePool.objects.get(nation=nation)
                if pool.consecutive_food_deficit_turns >= COLLAPSE_STARVATION_TURNS:
                    nation.is_alive = False
                    nation.save(update_fields=["is_alive"])
                    self._log(f"NATION COLLAPSED: {nation.name} (starvation for {pool.consecutive_food_deficit_turns} turns)")
            except NationResourcePool.DoesNotExist:
                pass

    def _create_next_turn(self, current_turn):
        """Create the next turn."""
        next_deadline = timezone.now() + timedelta(hours=self.game.turn_duration_hours)
        return Turn.objects.create(
            game=self.game,
            turn_number=current_turn.turn_number + 1,
            deadline=next_deadline,
        )

    def _log(self, message):
        """Add to resolution log."""
        logger.info(f"[Game {self.game.id}] {message}")
        self.log.append(message)
