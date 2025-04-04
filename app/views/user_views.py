from fastapi import APIRouter, Path
from typing import List
from app.schemas.user import CreateUserDto, UserDto, UserWithEmailDto
import app.controllers.user as user_controller

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserWithEmailDto)
async def create_user(user: CreateUserDto):
    """Создание пользователя"""
    return await user_controller.create_user(user)


@router.get("", response_model=List[UserDto])
async def list_users():
    """Получение всех пользователей"""
    return await user_controller.get_users()


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int = Path(..., gt=0)):
    """Удаление пользователя по ID"""
    await user_controller.delete_user(user_id)


@router.get("/{user_id}", response_model=UserDto)
async def get_user(user_id: int = Path(..., gt=0)):
    """Получение пользователя по ID (без email)"""
    return await user_controller.get_user_by_id(user_id)


@router.get("/{user_id}/full", response_model=UserWithEmailDto)
async def get_user_with_email(user_id: int = Path(..., gt=0)):
    """Получение пользователя по ID (с email)"""
    return await user_controller.get_user_with_email(user_id)
