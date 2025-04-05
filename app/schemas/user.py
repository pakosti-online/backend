from pydantic import BaseModel, StringConstraints
from typing import Optional, Annotated
from app.models.user import UserModel


class CreateUserDto(BaseModel):
    email: Annotated[str, StringConstraints(min_length=4, max_length=60)]
    password: Annotated[str, StringConstraints(min_length=8)]
    first_name: Annotated[str, StringConstraints(min_length=3, max_length=30)]
    last_name: Annotated[str, StringConstraints(min_length=3, max_length=30)]
    patronymic: Optional[
        Annotated[str, StringConstraints(min_length=3, max_length=30)]
    ]


class UserDto(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: Optional[str]

    @staticmethod
    def new(user: UserModel):
        return UserDto(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            patronymic=user.patronymic,
        )


class VerboseUserDto(UserDto):
    email: str
    balance: int

    @staticmethod
    def new(user: UserModel):
        return VerboseUserDto(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            patronymic=user.patronymic,
            email=user.email,
            balance=user.balance,
        )


class UserTokensDto(BaseModel):
    user_data: VerboseUserDto
    access_token: str
    refresh_token: str


class UserEditPublicDto(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
