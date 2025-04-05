from pydantic import BaseModel, StringConstraints
from typing import Optional, Annotated


class CreateUserDto(BaseModel):
    email: Annotated[str, StringConstraints(min_length=4, max_length=60)]
    password: Annotated[str, StringConstraints(min_length=8)]
    first_name: Annotated[str, StringConstraints(min_length=3, max_length=30)]
    last_name: Annotated[str, StringConstraints(min_length=3, max_length=30)]
    patronymic: Optional[
        Annotated[str, StringConstraints(min_length=3, max_length=30)]
    ]


class UserDto(BaseModel):
    first_name: str
    last_name: str
    patronymic: Optional[str]


class UserWithEmailDto(UserDto):
    email: str
