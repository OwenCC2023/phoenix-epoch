"""Helper functions to broadcast WebSocket messages to game rooms."""
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def _send_to_game(game_id, message):
    """Send a message to all connected clients in a game room."""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"game_{game_id}",
        message,
    )


def notify_turn_started(game_id, turn_number, deadline):
    _send_to_game(game_id, {
        "type": "turn_started",
        "turn_number": turn_number,
        "deadline": deadline.isoformat() if hasattr(deadline, 'isoformat') else str(deadline),
    })


def notify_turn_resolved(game_id, turn_number, resolution_log=None):
    _send_to_game(game_id, {
        "type": "turn_resolved",
        "turn_number": turn_number,
        "resolution_log": resolution_log or [],
    })


def notify_trade_received(game_id, trade_id, from_nation_name):
    _send_to_game(game_id, {
        "type": "trade_received",
        "trade_id": trade_id,
        "from_nation": from_nation_name,
    })


def notify_event_triggered(game_id, event_id, title, description):
    _send_to_game(game_id, {
        "type": "event_triggered",
        "event_id": event_id,
        "title": title,
        "description": description,
    })


def notify_player_joined(game_id, username):
    _send_to_game(game_id, {
        "type": "player_joined",
        "username": username,
    })


def notify_player_submitted(game_id, nation_name):
    _send_to_game(game_id, {
        "type": "player_submitted",
        "nation_name": nation_name,
    })


def notify_game_paused(game_id):
    _send_to_game(game_id, {"type": "game_paused"})


def notify_game_resumed(game_id, new_deadline=None):
    _send_to_game(game_id, {
        "type": "game_resumed",
        "new_deadline": new_deadline.isoformat() if hasattr(new_deadline, 'isoformat') else str(new_deadline) if new_deadline else None,
    })
