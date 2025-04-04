from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserOut
from app.controllers import user_controller



router = APIRouter(prefix="/users", tags=["Users"])



@router.post("/api/users", response_model=UserOut)
async def create_user(user: UserCreate):
    """Создание пользователя"""
    return await user_controller.create_user(user)


@router.get("/api/users", response_model=list[UserOut])
async def list_users():
    """Получение всех пользователей"""
    return await user_controller.get_users()

