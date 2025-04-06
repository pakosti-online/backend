from .websocket import manager_con as manager
from app.models.user import UserModel
from app.schemas.websocket import NotificationDto


async def event_sending_mes(
    message: str,
    user: UserModel,
) -> None:
    await manager.send_personal_message(message, user.id)
    

async def broadcast(message: str) -> None:
    await manager.broadcast(message)
