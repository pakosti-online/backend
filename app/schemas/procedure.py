from pydantic import BaseModel, Field
from fastapi import Depends



class ProcedureCreate(BaseModel):
    name: str
    category: str


class ProcedureId(BaseModel):
    id: str


class ProcedureOut(BaseModel):
    id: int
    name: str
    date_created: str
    date_updated: str
    category: str