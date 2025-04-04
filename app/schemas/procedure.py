from pydantic import BaseModel, Field
from fastapi import Depends



class Input_Procedure(BaseModel):
    name: str
    category: str


