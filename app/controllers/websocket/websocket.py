from typing import Dict
from fastapi import WebSocket
from app.schemas.websocket import WebSocketMessage

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(
        self, message: WebSocketMessage, user_id: int
    ):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            try:
                if isinstance(message, str):
                    await websocket.send_text(message)
                else:
                    await websocket.send_json(message.dict())
            except Exception as e:
                self.disconnect(user_id)

    async def broadcast(self, message: WebSocketMessage):
        for connection in self.active_connections.values():
            try:
                if isinstance(message, str):
                    await connection.send_text(message)
                else:
                    await connection.send_json(message.dict())
            except Exception:
                continue


manager_con = ConnectionManager()
