from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from app.models.user import UserModel
from app.models.finances import FinancesEducate

import app.controllers.analytics.common_analytics as analytics_controller

router = APIRouter(prefix="/finances", tags=["Finances"])
security = HTTPBearer()

@router.get("")
async def get_finances_ed():
    finances = await analytics_controller.get_finances_educate()
    return {"finances_ed": finances}


@router.get("/random")
async def get_random_finanses_ed():
    return await analytics_controller.get_random_finances_ed()