from .websocket import manager_con as manager
from app.models.user import UserModel
from app.schemas.websocket import NotificationDto


async def event_sending_mes(
    message: str,
    user: UserModel,
) -> None:
    manager.send_personal_message(message, user.id)


async def event_sending_notif(
    notification: NotificationDto,
    user: UserModel,
) -> None:
    manager.send_notification(notification, user.id)


async def broadcast(message: str) -> None:
    manager.broadcast(message)
