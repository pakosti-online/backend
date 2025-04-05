from fastapi import APIRouter, Depends
from app.schemas.transaction import (
    CreateTransactionDto,
    EditTransactionDto,
    TransactionCategoryOutDto,
)
import app.controllers.transaction as transaction_controller
import app.controllers.user as user_controller
import app.controllers.categories as category_controller
import app.controllers.ml as ml_controller

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("")
async def create_transaction(
    transaction: CreateTransactionDto,
    user=Depends(user_controller.auth.get_user),
):
    """Создание транзакции"""
    return await transaction_controller.create(transaction, user)


@router.patch("")
async def edit_category(
    data: EditTransactionDto, user=Depends(user_controller.auth.get_user)
):
    await transaction_controller.edit_category(
        user, data.id, data.category_name
    )


@router.get("")
async def get_by_user(user=Depends(user_controller.auth.get_user)):
    return await transaction_controller.get_transactions_by_user(user.id)


@router.get("/categories", response_model=list[TransactionCategoryOutDto])
async def get_all_categories():
    """Получение всех категорий"""
    return await category_controller.get_all_categories()


@router.get("/recommendations")
async def get_recommendations(user=Depends(user_controller.auth.get_user)):
    transactions = await transaction_controller.get_transactions_by_user(
        user.id
    )
    return await ml_controller.get_recommendations(transactions)
