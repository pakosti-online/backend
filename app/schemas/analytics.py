from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import List, Optional, Literal


class CategoryStat(BaseModel):
    name: str
    amount: float
    percentage: float
    is_deposit: bool


class DailyStat(BaseModel):
    date: str
    total_income: float
    total_expense: float


class AnalyticsResponse(BaseModel):
    period_start: str
    period_end: str
    total_income: float
    total_expense: float
    balance_change: float
    categories: List[CategoryStat]
    daily_stats: List[DailyStat]


class BaseNotification(BaseModel):
    type: str
    timestamp: datetime = datetime.now()


class ErrorNotification(BaseNotification):
    type: Literal["error"] = "error"
    message: str


class AnalyticsNotification(BaseNotification):
    type: Literal["analytics_update"] = "analytics_update"
    data: AnalyticsResponse  # Используем уже созданную схему аналитики


class NotificationDto(BaseModel):
    type: Literal["info", "warning", "success"]
    title: str
    message: str
    duration: Optional[int] = 5000  # В миллисекундах


class CategoryAnalytics(BaseModel):
    category_name: str
    is_deposit: bool
    user_total: Decimal
    others_average: Decimal
    difference_percent: Optional[
        float
    ]  # может быть None, если сравнение невозможно


class AnalyticsResponses(BaseModel):
    analytics: List[CategoryAnalytics]


class BalanceStructureAnalytics(BaseModel):
    balance: Decimal

    mandatory_income: Decimal
    non_mandatory_income: Decimal
    mandatory_expense: Decimal
    non_mandatory_expense: Decimal

    mandatory_income_percent: float
    non_mandatory_income_percent: float
    mandatory_expense_percent: float
    non_mandatory_expense_percent: float
