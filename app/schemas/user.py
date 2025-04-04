from pydantic import BaseModel, Field
from fastapi import Depends

from typing import List
from enum import Enum


class UserCreate(BaseModel):
    name: str
    email: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
