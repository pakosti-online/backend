from .auth import create_refresh_token, create_access_token, verify_token
from app.schemas.user import CreateUserDto, VerboseUserDto, UserDto
from app.models.user import UserModel
from fastapi import HTTPException
from passlib.hash import bcrypt
from os import environ

DEFAULT_BALANCE = int(environ.get("DEFAULT_BALANCE", '10000'))


async def create_user(dto: CreateUserDto) -> VerboseUserDto:
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
        balance=DEFAULT_BALANCE
    )

    return VerboseUserDto.new(user)


async def get_users() -> list[UserDto]:
    users = await UserModel.all()
    return [UserDto.new(user) for user in users]


async def delete_user(user_id: int) -> None:
    user = await UserModel.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    await user.delete()


async def get_user_by_id(user_id: int) -> UserDto:
    user = await UserModel.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return UserDto.new(user)


async def get_user_verbose(user_id: int) -> VerboseUserDto:
    user = await UserModel.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return VerboseUserDto.new(user)


async def login(email: str, password: str):
    user = await UserModel.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    elif not user.verify_password(password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    return user, create_access_token(user), create_refresh_token(user)


async def refresh(refresh_token: str):
    payload = verify_token(refresh_token, "refresh")
    user_data: dict = payload.get("user")
    user = await UserModel.get_or_none(user_data.get("email"))
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return create_access_token(user)
