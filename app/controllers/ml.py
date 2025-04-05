from fastapi import HTTPException
from app.schemas.transaction import TransactionDto
from os import environ
import httpx
import json

PREDICTOR_CATEGORIZER_URL = environ.get(
    "EXTERNAL_PREDICTOR_CATEGORIZER_URL", "http://localhost:3000/"
)

PREDICTOR_RECOMMENDATION_URL = environ.get(
    "EXTERNAL_PREDICTOR_RECOMMENDATION_URL", "http://localhost:3000/"
)


async def get_category_by_product(product_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            PREDICTOR_CATEGORIZER_URL, json={"word": product_name}
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=403,
                detail="Произошла ошибка при попытке распознать категорию!",
            )
        return response.text


async def get_recommendations(transactions: list[TransactionDto]):
    loadable_transactions = [
        transaction.model_dump() for transaction in transactions
    ]
    async with httpx.AsyncClient() as client:
        response = await client.post(
            PREDICTOR_RECOMMENDATION_URL, json=loadable_transactions
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=403,
                detail="Произошла ошибка при попытке получить рекомендации!",
            )
        return json.loads(response.text)
