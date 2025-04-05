from app.schemas.transaction import TransactionCategoryOutDto
from app.models.transaction import TransactionCategoryModel
from os import environ
import httpx

PREDICTOR_CATEGORIZER_URL = environ.get(
    "EXTERNAL_PREDICTOR_CATEGORIZER_URL", "http://localhost:3000/"
)


async def get_category(product_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            PREDICTOR_CATEGORIZER_URL, json={"word": product_name}
        )

        category_name = response.text
        return await TransactionCategoryModel.get_or_none(name=category_name)


async def get_all_categories() -> list[TransactionCategoryOutDto]:
    transaction_categories = await TransactionCategoryModel.all()

    return [
        TransactionCategoryOutDto(transaction_category)
        for transaction_category in transaction_categories
    ]
