from pydantic import BaseModel, Field
from fastapi import Depends
from datetime import datetime


class TransactionCreate(BaseModel):
    name: str
    category: str
    user_id: int


class TransactionId(BaseModel):
    id: int


class TransactionOut(BaseModel):
    id: int
    name: str
    date_created: datetime
    date_updated: datetime
    category: str
    user_id: int


class TransactionChangeById(BaseModel):
    id: int
    name: Depends[str, None]
