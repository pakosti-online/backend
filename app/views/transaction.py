from fastapi import APIRouter, Depends
from app.schemas.transaction import (
    CreateTransactionDto,
)
import app.controllers.transaction as transaction_controller
import app.controllers.user as user_controller

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("")
async def create_transaction(
    transaction: CreateTransactionDto,
    user=Depends(user_controller.auth.get_user),
):
    """Создание транзакции"""
    return await transaction_controller.create(transaction, user)
