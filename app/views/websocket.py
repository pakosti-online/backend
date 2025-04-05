from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.controllers.user.auth import get_user
from app.controllers.websocket.websocket import manager_con as manager
from app.models.user import UserModel

router = APIRouter(prefix="/notifications", tags=["Websockets"])


@router.websocket("/{current_user.id}")
async def notifications_websocket_endpoint(
    websocket: WebSocket, current_user: UserModel = Depends(get_user)
):
    await manager.connect(current_user.id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(current_user.id)
