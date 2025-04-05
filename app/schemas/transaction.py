from pydantic import BaseModel, StringConstraints, condecimal, PlainSerializer
from app.models.transaction import TransactionModel, TransactionCategoryModel
from typing import Annotated, Optional
from datetime import datetime


class CreateTransactionDto(BaseModel):
    product_name: Annotated[
        str, StringConstraints(min_length=2, max_length=100)
    ]
    delta: Optional[condecimal(max_digits=20, decimal_places=2)] = None


class EditTransactionDto(BaseModel):
    id: int
    category_name: str


SerializableDatetime = Annotated[
    datetime,
    PlainSerializer(
        lambda _datetime: _datetime.strftime("%m/%d/%Y, %H:%M:%S"),
        return_type=str,
    ),
]


class TransactionDto(BaseModel):
    id: int
    product_name: str
    date_created: SerializableDatetime
    category: str
    balance: float
    delta: float
    user_id: int

    @staticmethod
    def new(data: TransactionModel, category_name: str):
        return TransactionDto(
            id=data.id,
            product_name=data.product_name,
            date_created=data.date_created,
            category=category_name,
            balance=data.balance,
            delta=data.delta,
            user_id=data.user_id,
        )


class TransactionCategoryOutDto(BaseModel):
    id: int
    name: Annotated[str, StringConstraints(max_length=100)]
    is_deposit: bool

    @staticmethod
    def new(data: TransactionCategoryModel):
        return TransactionCategoryOutDto(
            id=data.id,
            name=data.name,
            is_deposit=data.is_deposit,
        )
