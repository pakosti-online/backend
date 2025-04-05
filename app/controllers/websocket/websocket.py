from typing import Dict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: int):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

    async def send_notification(self, notification: dict, user_id: int):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(notification)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager_con = ConnectionManager()
