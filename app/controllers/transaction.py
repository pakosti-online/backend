from fastapi import HTTPException

from app.models.transaction import TransactionModel
from app.models.user import UserModel
from app.schemas.transaction import (
    CreateTransactionDto,
    TransactionDto,
)
from app.controllers.categories import get_category
import app.controllers.websocket.events as events


async def create(data: CreateTransactionDto, user: UserModel) -> TransactionDto:
    if data.delta <= 0:
        events.event_sending_mes("Принимаются только delta > 0!", user)
        raise HTTPException(
            status_code=403, detail="Принимаются только delta > 0!"
        )

    category = await get_category(data.product_name)
    if not category:
        events.event_sending_mes(
            "Не удалось получить данные о категории!", user
        )
        raise HTTPException(
            status_code=403, detail=f"Не удалось получить данные о категории!"
        )

    delta = data.delta * (1 if category.is_deposit else -1)
    new_balance = user.balance + delta

    if new_balance < 0:
        events.event_sending_mes("На балансе недостаточно средств!", user)
        raise HTTPException(
            status_code=403, detail="На балансе недостаточно средств!"
        )

    user.balance = new_balance
    await user.save()

    transaction = await TransactionModel.create(
        product_name=data.product_name,
        balance=new_balance,
        delta=delta,
        user_id=user.id,
        category_id=category.id,
    )

    return TransactionDto.new(transaction, category.name)
