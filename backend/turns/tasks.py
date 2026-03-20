"""Celery tasks for turn management."""
import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def resolve_turn(self, game_id):
    """Resolve the current turn for a game. Scheduled at turn deadline."""
    from games.models import Game
    from .engine import TurnResolutionEngine

    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        logger.error(f"Game {game_id} not found for turn resolution")
        return

    if game.status != Game.Status.ACTIVE:
        logger.info(f"Game {game_id} is not active, skipping resolution")
        return

    engine = TurnResolutionEngine(game)
    try:
        turn = engine.resolve_current_turn()
        if turn:
            logger.info(f"Turn {turn.turn_number} resolved for game {game_id}")
            # Schedule next turn resolution
            from django.utils import timezone
            next_turn = game.turns.filter(status="pending").first()
            if next_turn:
                resolve_turn.apply_async(
                    args=[game_id],
                    eta=next_turn.deadline,
                    task_id=f"resolve-turn-{game_id}-{next_turn.turn_number}",
                )
    except Exception as e:
        logger.exception(f"Turn resolution failed for game {game_id}: {e}")
        raise self.retry(exc=e, countdown=60)


@shared_task
def check_early_resolution(game_id):
    """Check if all players have submitted and resolve early if so."""
    from games.models import Game
    from nations.models import Nation
    from .models import Turn, TurnSubmission

    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return

    turn = Turn.objects.filter(game=game, status=Turn.Status.PENDING).first()
    if not turn:
        return

    alive_nations = Nation.objects.filter(game=game, is_alive=True).count()
    submissions = TurnSubmission.objects.filter(turn=turn).count()

    if submissions >= alive_nations and alive_nations > 0:
        logger.info(f"All players submitted for game {game_id} Turn {turn.turn_number} — resolving early")
        # Revoke the scheduled task
        from phoenix_epoch.celery import app
        task_id = f"resolve-turn-{game_id}-{turn.turn_number}"
        app.control.revoke(task_id)
        # Resolve now
        resolve_turn.delay(game_id)
