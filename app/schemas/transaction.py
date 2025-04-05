from pydantic import BaseModel, StringConstraints, condecimal
from typing import Annotated, Optional, Dict, Union
from fastapi import Depends
from datetime import datetime

from app.models.transaction import TransactionModel


class TransactionCreateDto(BaseModel):
    name: Annotated[str, StringConstraints(min_length=2, max_length=100)]
    category: Annotated[str, StringConstraints(max_length=60)]
    balance: Optional[condecimal(max_digits=20, decimal_places=2)] = None
    delta: Optional[condecimal(max_digits=20, decimal_places=2)] = None
    user_id: int

    @staticmethod
    def new(data: TransactionModel):
        return TransactionCreateDto(
            name=data.name,
            category=data.category,
            balance=data.balance,
            delta=data.delta,
            user_id=data.user_id,
        )


class TransactionUserIdDto(BaseModel):
    user_id: int


class TransactionIdDto(BaseModel):
    id: int


class TransactionOutDto(BaseModel):
    id: int
    name: str
    date_created: datetime
    date_updated: datetime
    category: str
    balance: float
    delta: float
    user_id: int

    @staticmethod
    def new(data: TransactionModel):
        return TransactionOutDto(
            id=data.id,
            name=data.name,
            date_created=data.date_created,
            date_updated=data.date_updated,
            category=data.category,
            balance=data.balance,
            delta=data.delta,
            user_id=data.user_id,
        )


class TransactionChangeByIdDto(BaseModel):
    id: int  # id пользователя, возможно изменить в инпуте
    updates: Dict[str, Union[str, int, float, None]]  # Словарь: ключ-значение
