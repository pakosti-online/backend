from app.schemas.transaction import TransactionCategoryOutDto
from app.models.transaction import TransactionCategoryModel
import app.controllers.ml as ml_controller


async def get_by_product_name(product_name: str):
    category_name = await ml_controller.get_category_by_product(product_name)
    return await TransactionCategoryModel.get_or_none(name=category_name)


async def get_all_categories() -> list[TransactionCategoryOutDto]:
    transaction_categories = await TransactionCategoryModel.all()

    return [
        TransactionCategoryOutDto.new(transaction_category)
        for transaction_category in transaction_categories
    ]
