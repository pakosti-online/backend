from app.models.user import UserModel
from app.schemas.user import CreateUserDto, UserWithEmailDto, UserDto
from typing import List

from fastapi import HTTPException
from passlib.hash import bcrypt


async def create_user(dto: CreateUserDto) -> UserWithEmailDto:
    existing = await UserModel.get_or_none(email=dto.email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с данным email уже существует!",
        )

    user = await UserModel.create(
        email=dto.email,
        password_hash=bcrypt.hash(dto.password),
        first_name=dto.first_name,
        last_name=dto.last_name,
        patronymic=dto.patronymic or "",
    )

    return UserWithEmailDto(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        patronymic=user.patronymic or None,
    )


async def get_users() -> List[UserDto]:
    users = await UserModel.all()
    return [
        UserDto(
            first_name=user.first_name,
            last_name=user.last_name,
            patronymic=user.patronymic or None,
        )
        for user in users
    ]


async def delete_user(user_id: int) -> None:
    user = await UserModel.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    await user.delete()


async def get_user_by_id(user_id: int) -> UserDto:
    user = await UserModel.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return UserDto(
        first_name=user.first_name,
        last_name=user.last_name,
        patronymic=user.patronymic or None,
    )


async def get_user_with_email(user_id: int) -> UserWithEmailDto:
    user = await UserModel.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return UserWithEmailDto(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        patronymic=user.patronymic or None,
    )
