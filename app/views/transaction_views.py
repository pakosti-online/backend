from fastapi import APIRouter
from app.schemas.transaction import (
    TransactionCreate,
    TransactionId,
    TransactionOut,
    TransactionChangeById,
)
import app.controllers.transaction as transaction_controller

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("", response_model=TransactionOut)
async def create_transaction(transaction: TransactionCreate):
    """Создание транзакции"""
    return await transaction_controller.create(transaction)


@router.get("", response_model=list[TransactionOut])
async def list_transactions():
    """Получение всех транзакций"""
    return await transaction_controller.get_all()


@router.post("-get-by-userId", response_model=list[TransactionOut])
async def get_transactions_with_user_id(data: TransactionId):
    """Получение транзакций относительно id пользователя"""
    return await transaction_controller.get_transactions_for_user_id(data)


@router.patch("/change", response_model=TransactionOut)
async def change_transaction_data(data: TransactionChangeById):
    """Изменение некоторых параметров, относительно id транзакции"""
    return await transaction_controller.change_tranzaction_by_id(data)
