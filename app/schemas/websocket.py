from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime
from app.schemas.analytics import ErrorNotification, AnalyticsNotification


class NotificationDto(BaseModel):
    message: str
    type: str  # "error", "warning", "info", "success"
    transaction_id: Optional[int] = None
    timestamp: datetime

    @staticmethod
    def new(
        input_message,
        input_type,
        input_transaction_id,
    ):
        return NotificationDto(
            message=input_message,
            type=input_type,
            transaction_id=input_transaction_id,
            timestamp=datetime.now(),
        )

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


# Объединенный тип для всех уведомлений
WebSocketMessage = Union[
    ErrorNotification, AnalyticsNotification, NotificationDto
]
