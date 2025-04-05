from fastapi import HTTPException

from app.models.transaction import TransactionModel
from app.models.user import UserModel
from app.schemas.transaction import (
    TransactionCreateDto,
    TransactionUserIdDto,
    TransactionOutDto,
    TransactionChangeByIdDto,
    TransactionIdDto,
)


async def create(data: TransactionCreateDto) -> TransactionOutDto:
    """Создание транзакции"""
    user = await UserModel.get_or_none(id=data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"Пользователь не найден")

    try:
        transaction = await TransactionModel.create(
            name=data.name,
            category=data.category,
            user_id=data.user_id,
            balance=data.balance,
            delta=data.delta,
        )
        return TransactionOutDto.new(transaction)

    except Exception:
        raise HTTPException(
            status_code=404, detail="Неправильный формат данных"
        )


async def update_transaction(
    data: TransactionChangeByIdDto,
) -> TransactionOutDto:
    """Изменение полей у транзакции, передаются id транзакции и словарь: ключ-значения"""
    transaction = await TransactionModel.get_or_none(id=data.id)

    if not transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")

    valid_fields = {
        field
        for field in TransactionModel._meta.fields_map.keys()
        if field != "id"
    }

    # Проверка на существование полей в модельке
    for field in data.updates.keys():
        if field not in valid_fields:
            raise HTTPException(
                status_code=404,
                detail=f"Неверное поле: '{field}'. Допустимые поля: {valid_fields}",
            )

    for field, value in data.updates.items():
        setattr(transaction, field, value)

    await transaction.save()

    return TransactionOutDto.new(transaction)


async def get_transactions_for_user_id(
    data: TransactionUserIdDto,
) -> list[TransactionOutDto]:
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

    return [TransactionOutDto.new(transaction) for transaction in transactions]


async def get_all() -> list[TransactionOutDto]:
    """Получение всех транзакций"""
    transactions = await TransactionModel.all()

    return [TransactionOutDto.new(transaction) for transaction in transactions]


async def delete_transaction(data: TransactionIdDto) -> None:
    transaction = await TransactionModel.get_or_none(id=data.id)

    if not transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")

    await transaction.delete()
