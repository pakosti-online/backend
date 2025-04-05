from app.models.transaction import TransactionModel, TransactionCategoryModel
import app.controllers.categories as category_controller
import app.controllers.websocket.events as events
from app.models.user import UserModel
from fastapi import HTTPException
from app.schemas.transaction import (
    CreateTransactionDto,
    TransactionDto,
)


async def create(data: CreateTransactionDto, user: UserModel) -> TransactionDto:
    if data.delta <= 0:
        events.event_sending_mes("Принимаются только delta > 0!", user)
        raise HTTPException(
            status_code=403, detail="Принимаются только delta > 0!"
        )

    category = await category_controller.get_by_product_name(data.product_name)
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
    events.event_sending_mes("Успешно создана транзакция!", user)
    return TransactionDto.new(transaction, category.name)


async def edit_category(
    user: UserModel, transaction_id: int, category_name: str
):
    transaction = await TransactionModel.get_or_none(id=transaction_id)

    if not transaction:
        events.event_sending_mes("Несуществующая транзакция!", user)
        raise HTTPException(
            status_code=404, detail="Транзакции с данным ID не существует!"
        )

    if transaction.user_id != user.id:
        events.event_sending_mes(
            "Вы не имеете права взаимодействовать с данной транзакцией!", user
        )
        raise HTTPException(
            status_code=403,
            detail="Вы не имеете права взаимодействовать с данной транзакцией!",
        )

    current_category = await TransactionCategoryModel.get(
        id=transaction.category_id
    )

    if current_category.is_deposit:
        events.event_sending_mes(
            "Вы не можете менять категорию у приходящей транзакции!", user
        )
        raise HTTPException(
            status_code=403,
            detail="Вы не можете менять категорию у приходящей транзакции!",
        )
    elif new_category.is_deposit:
        events.event_sending_mes(
            "Вы не можете менять категорию на приходящую транзакцию!", user
        )
        raise HTTPException(
            status_code=403,
            detail="Вы не можете менять категорию на приходящую!",
        )

    new_category = await TransactionCategoryModel.get_or_none(
        name=category_name
    )

    if not new_category:
        events.event_sending_mes("Такой категории не существует!", user)
        raise HTTPException(
            status_code=404, detail="Данной категории не существует!"
        )

    transaction.category_id = new_category.id
    events.event_sending_mes("Успешно сохранена транзакция!", user)
    await transaction.save()


async def get_transactions_by_user(user_id: int) -> list[TransactionDto]:
    transactions = await TransactionModel.filter(user_id=user_id)
    return [
        TransactionDto.new(transaction, (await transaction.category).name)
        for transaction in transactions
    ]
