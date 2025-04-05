from jose.exceptions import ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user import UserWithEmailDto
from tortoise.exceptions import DoesNotExist
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from typing import Literal, TypeAlias
from app.models.user import UserModel
from jose import jwt, JWTError
from os import environ

TokenType: TypeAlias = Literal["access"] | Literal["refresh"]

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="users/login")
JWT_TOKEN_SECRET = environ.get("JWT_TOKEN_SECRET", "pakost")


def create_token(
    user: UserModel, lifetime: timedelta, token_type: TokenType
) -> str:
    exp = datetime.now() + lifetime
    data = {
        "user": UserWithEmailDto(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            patronymic=user.patronymic,
            email=user.email,
        ).model_dump(),
        "exp": exp,
        "type": token_type,
    }

    return jwt.encode(data, JWT_TOKEN_SECRET)


def create_access_token(user: UserModel):
    return create_token(user, timedelta(minutes=15), "access")


def create_refresh_token(user: UserModel):
    return create_token(user, timedelta(days=14), "refresh")


def verify_token(token: str, token_type: TokenType):
    try:
        payload = jwt.decode(token, JWT_TOKEN_SECRET)
        if payload.get("type") != token_type:
            raise HTTPException(status_code=403, detail="Неверный тип токена!")
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Истекло время жизни токена!"
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Токен невалиден!")


async def get_user(token: str = Depends(OAUTH2_SCHEME)):
    try:
        payload = verify_token(token, "access")
        user_data = payload.get("user")
        return await UserModel.get(id=user_data.get("id"))
    except DoesNotExist:
        raise HTTPException(
            status_code=401, detail="Пользователя не существует!"
        )
