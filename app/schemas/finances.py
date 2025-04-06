from pydantic import BaseModel
from app.models.finances import FinancesEducate


class FinancesEducateDto(BaseModel):
    title: str
    description: str
    
    @staticmethod
    def new(data: FinancesEducate):
        return FinancesEducateDto(
            title=data.title,
            description=data.description,
        )