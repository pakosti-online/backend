from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from app.schemas.analytics import AnalyticsResponse, AnalyticsResponses
from app.models.user import UserModel

import app.controllers.analytics.common_analytics as analytics_controller
import app.controllers.analytics.comprative_analytics as comp_analytics_controller

import app.controllers.user as user_controller

router = APIRouter(prefix="/analytics", tags=["Analytics"])
security = HTTPBearer()


@router.get("", response_model=AnalyticsResponse)
async def get_user_analytics(
    period_days: int = 7,
    current_user: UserModel = Depends(user_controller.auth.get_user),
):
    """Эндпоинт по созданию простенькой аналитики данных относительно даты (кол-во дней) у нынешнего пользователя"""
    return await analytics_controller.get_analytics(
        current_user.id, period_days
    )


@router.get("/comprative", response_model=AnalyticsResponses)
async def get_analytics(user=Depends(user_controller.get_user)):
    analytics = await comp_analytics_controller.get_user_analytics(user)
    return {"analytics": analytics}
