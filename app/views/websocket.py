from fastapi import APIRouter
from fastapi import WebSocket

from app.schemas.websocket import (
    NotificationsDto,
)

router = APIRouter(prefix="/ws", tags=["Websockets"])

@router.websocket("", response_model=NotificationsDto)
async def send_notification(websocket: WebSocket, ):
    await websocket.accept()

    await websocket.send_persona("something")


    try:
        while True:
            pass
    
    except:
        pass