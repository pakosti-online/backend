from fastapi import HTTPException

from app.models.transaction import TransactionModel
from app.models.user import UserModel
from app.schemas.transaction import (
    TransactionCreate,
    TransactionId,
    TransactionOut,
    TransactionChangeById,
)


async def create(data: TransactionCreate) -> TransactionModel:
    """Создание транзакции"""
    user = await UserModel.get_or_none(id=data.id)
    if not user:
        raise HTTPException(status_code=404, detail=f"Пользователь не найден")

    try:
        transaction = await TransactionModel.create(
            name=data.name, category=data.category, user_id=data.user_id
        )
        return transaction

    except Exception:
        raise HTTPException(
            status_code=404, detail="Неправильный формат данных"
        )


# недоделано !!!
async def change_tranzaction_by_id(
    data: TransactionChangeById,
) -> TransactionModel:
    """Изменение параметров относительно id транзакции"""
    transaction_old = await TransactionModel.get_or_none(id=data.id)
    if not transaction_old:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")

    return


async def get_transactions_for_user_id(
    data: TransactionId,
) -> list[TransactionOut]:
    """Получение транзакций относительно id пользователя"""
    user = await UserModel.get_or_none(id=data.id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    transactions = await TransactionModel.filter(user_id=data.id).all()
    if not transactions:
        raise HTTPException(
            status_code=404,
            detail=f"Нет транзакций с закрепленной id пользователем: {data.id}",
        )

    return [
        TransactionOut(
            id=transaction.id,
            name=transaction.name,
            date_created=transaction.date_created,
            date_updated=transaction.date_updated,
            category=transaction.category,
            user_id=transaction.user_id,
        )
        for transaction in transactions
    ]


async def get_all() -> list[TransactionOut]:
    """Получение всех транзакций"""
    transactions = await TransactionModel.all()

    return [
        TransactionOut(
            id=transaction.id,
            name=transaction.name,
            date_created=transaction.date_created,
            date_updated=transaction.date_updated,
            category=transaction.category,
            user_id=transaction.user_id,
        )
        for transaction in transactions
    ]
