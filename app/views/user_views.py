from fastapi import APIRouter
from app.schemas.user import UserCreate, UserOut
import app.controllers.user as user_controller

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("", response_model=UserOut)
async def create_user(user: UserCreate):
    """Создание пользователя"""
    return await user_controller.create(user)


@router.get("", response_model=list[UserOut])
async def list_users():
    """Получение всех пользователей"""
    return await user_controller.get()

