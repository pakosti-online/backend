from .websocket import manager_con as manager
from app.schemas.websocket import NotificationDto
from app.models.user import UserModel
from app.models.transaction import TransactionModel


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


async def event_broadcast(message: str):
    manager.broadcast(message)


async def some_event(user: UserModel):

    pass
