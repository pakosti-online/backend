from datetime import datetime, timedelta
from fastapi import HTTPException
from tortoise.expressions import Q
from app.models.transaction import TransactionModel
from app.schemas.analytics import AnalyticsResponse, CategoryStat, DailyStat
from app.controllers.websocket.events import event_sending_mes
from app.models.user import UserModel
from app.schemas.analytics import AnalyticsNotification
from app.controllers.websocket.websocket import manager_con as manager


async def send_analytics_update(user: UserModel):
    try:
        analytics = await get_analytics(user.id)
        notification = AnalyticsNotification(
            type="analytics_update", data=analytics.dict()
        )
        manager.send_notification(notification, user.id)
    except Exception as e:
        error_msg = f"Ошибка обновления аналитики: {str(e)}"
        await event_sending_mes(error_msg, user)


async def get_analytics(
    user_id: int, period_days: int = 30
) -> AnalyticsResponse:
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)

        # Получаем все транзакции пользователя за период
        transactions = await TransactionModel.filter(
            user_id=user_id,
            date_created__gte=start_date,
            date_created__lte=end_date,
        ).prefetch_related("category")

        if not transactions:
            await event_sending_mes(
                f"Нет данных за выбранный период {period_days} дней", user_id
            )
            raise HTTPException(status_code=404, detail="No transactions found")

        # Считаем общие суммы
        total_income = sum(t.delta for t in transactions if t.delta > 0)
        total_expense = abs(sum(t.delta for t in transactions if t.delta < 0))
        balance_change = total_income - total_expense

        # Статистика по категориям
        categories_stats = {}
        for t in transactions:
            cat = await t.category
            if cat.name not in categories_stats:
                categories_stats[cat.name] = {
                    "amount": 0,
                    "is_deposit": cat.is_deposit,
                }
            categories_stats[cat.name]["amount"] += abs(t.delta)

        # Преобразуем в список и считаем проценты
        total_all = sum(v["amount"] for v in categories_stats.values())
        category_stats_list = [
            CategoryStat(
                name=name,
                amount=data["amount"],
                percentage=(
                    (data["amount"] / total_all) * 100 if total_all > 0 else 0
                ),
                is_deposit=data["is_deposit"],
            )
            for name, data in categories_stats.items()
        ]

        # Статистика по дням
        daily_stats = {}
        current_date = start_date
        while current_date <= end_date:
            daily_stats[current_date.strftime("%Y-%m-%d")] = {
                "income": 0,
                "expense": 0,
            }
            current_date += timedelta(days=1)

        for t in transactions:
            date_key = t.date_created.strftime("%Y-%m-%d")
            if t.delta > 0:
                daily_stats[date_key]["income"] += t.delta
            else:
                daily_stats[date_key]["expense"] += abs(t.delta)

        daily_stats_list = [
            DailyStat(
                date=date,
                total_income=data["income"],
                total_expense=data["expense"],
            )
            for date, data in daily_stats.items()
        ]

        return AnalyticsResponse(
            period_start=start_date.strftime("%Y-%m-%d"),
            period_end=end_date.strftime("%Y-%m-%d"),
            total_income=total_income,
            total_expense=total_expense,
            balance_change=balance_change,
            categories=category_stats_list,
            daily_stats=daily_stats_list,
        )

    except Exception as e:
        await event_sending_mes(
            f"Ошибка при получении аналитики: {str(e)}", user_id
        )
        raise HTTPException(status_code=500, detail=str(e))
