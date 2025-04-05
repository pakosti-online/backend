from app.models.transaction import TransactionCategoryModel
from app.schemas.transaction import TransactionCategoryOutDto


# TODO
async def get_category(product_name: str):
    return await TransactionCategoryModel.get_or_none(name="Зарплата")


async def get_all_categories() -> list[TransactionCategoryOutDto]:
    transaction_categories = await TransactionCategoryModel.all()

    return [
        TransactionCategoryOutDto(transaction_category)
        for transaction_category in transaction_categories
    ]
