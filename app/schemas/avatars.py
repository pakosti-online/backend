from pydantic import BaseModel
from app.models.user import AvatarModel


class UserAvatarInDto(BaseModel):
    id: int


class UserInDto(BaseModel):
    id: int


class UserAvatarOutDto(BaseModel):
    id: int
    file_path: str

    @staticmethod
    def new(data: AvatarModel):
        return UserAvatarOutDto(
            id=data.id,
            file_path=data.file_path,
        )
