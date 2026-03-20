"""WebSocket consumer for game rooms."""
import json
import logging

from channels.generic.websocket import AsyncJsonWebsocketConsumer

logger = logging.getLogger(__name__)


class GameConsumer(AsyncJsonWebsocketConsumer):
    """WebSocket consumer for real-time game events."""

    async def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.room_group_name = f"game_{self.game_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logger.info(f"WebSocket connected: game {self.game_id}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        logger.info(f"WebSocket disconnected: game {self.game_id}")

    async def receive_json(self, content):
        """Handle incoming WebSocket messages from clients."""
        msg_type = content.get("type")
        if msg_type == "ping":
            await self.send_json({"type": "pong"})

    # Event handlers — called when channel layer sends group messages

    async def turn_started(self, event):
        await self.send_json({
            "type": "turn_started",
            "turn_number": event["turn_number"],
            "deadline": event["deadline"],
        })

    async def turn_resolved(self, event):
        await self.send_json({
            "type": "turn_resolved",
            "turn_number": event["turn_number"],
            "resolution_log": event.get("resolution_log", []),
        })

    async def trade_received(self, event):
        await self.send_json({
            "type": "trade_received",
            "trade_id": event["trade_id"],
            "from_nation": event["from_nation"],
        })

    async def event_triggered(self, event):
        await self.send_json({
            "type": "event_triggered",
            "event_id": event["event_id"],
            "title": event["title"],
            "description": event["description"],
        })

    async def player_joined(self, event):
        await self.send_json({
            "type": "player_joined",
            "username": event["username"],
        })

    async def player_submitted(self, event):
        await self.send_json({
            "type": "player_submitted",
            "nation_name": event["nation_name"],
        })

    async def game_paused(self, event):
        await self.send_json({"type": "game_paused"})

    async def game_resumed(self, event):
        await self.send_json({
            "type": "game_resumed",
            "new_deadline": event.get("new_deadline"),
        })
