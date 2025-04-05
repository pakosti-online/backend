from pydantic import BaseModel, StringConstraints, condecimal
from typing import Annotated, Optional, Dict, Union
from datetime import datetime


from app.models.user import UserModel, Avatar


class UserAvatarInDto(BaseModel):
    id: int


class UserAvatarOutDto(BaseModel):
    id: int
    file_path: str

    @staticmethod
    def new(data: Avatar):
        return UserAvatarOutDto(
            id=data.id,
            file_path=data.file_path,
        )
