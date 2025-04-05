from app.models.transaction import TransactionCategoryModel


# TODO
async def get_category(product_name: str):
    return await TransactionCategoryModel.get_or_none(name="Зарплата")
