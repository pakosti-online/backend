from app.models.transaction import TransactionModel, TransactionCategoryModel
from app.models.user import UserModel
from decimal import Decimal, DivisionByZero
from tortoise.expressions import Q
from app.schemas.analytics import CategoryAnalytics
from typing import List, Optional


async def get_user_analytics(user: UserModel) -> List[CategoryAnalytics]:
    categories = await TransactionCategoryModel.all()
    results = []

    for category in categories:
        # Сумма текущего пользователя
        user_total_qs = await TransactionModel.filter(
            user=user, category=category
        ).values("delta")
        user_total = sum([row["delta"] for row in user_total_qs]) if user_total_qs else Decimal("0.00")

        # Средняя сумма других пользователей
        others_total_qs = await TransactionModel.filter(
            ~Q(user=user), category=category
        ).values("delta")

        if others_total_qs:
            others_sum = sum([row["delta"] for row in others_total_qs])
            others_count = len(others_total_qs)
            others_avg = others_sum / others_count
        else:
            others_avg = Decimal("0.00")

        # Сравнение в процентах
        if others_avg != 0:
            diff_percent = float(((user_total - others_avg) / others_avg) * 100)
        else:
            diff_percent = None  # невозможно рассчитать

        results.append(
            CategoryAnalytics(
                category_name=category.name,
                is_deposit=category.is_deposit,
                user_total=user_total,
                others_average=others_avg,
                difference_percent=round(diff_percent, 2) if diff_percent is not None else None
            )
        )

    return results
