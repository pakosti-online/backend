from fastapi import APIRouter
from app.schemas.transaction import (
    TransactionCreateDto,
    TransactionUserIdDto,
    TransactionOutDto,
    TransactionChangeByIdDto,
)
import app.controllers.transaction as transaction_controller

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("", response_model=TransactionOutDto)
async def create_transaction(transaction: TransactionCreateDto):
    """Создание транзакции"""
    return await transaction_controller.create(transaction)


@router.get("", response_model=list[TransactionOutDto])
async def list_transactions():
    """Получение всех транзакций"""
    return await transaction_controller.get_all()


@router.post("-get-by-userId", response_model=list[TransactionOutDto])
async def get_transactions_with_user_id(data: TransactionUserIdDto):
    """Получение транзакций относительно id пользователя"""
    return await transaction_controller.get_transactions_for_user_id(data)


@router.patch("/{data.id}", response_model=TransactionOutDto)
async def change_transaction_data(data: TransactionChangeByIdDto):
    """Изменение некоторых параметров, относительно id транзакции"""
    return await transaction_controller.update_transaction(data)
