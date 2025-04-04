from app.models.user import UserModel
from app.schemas.user import UserCreate



async def create(data: UserCreate) -> UserModel:
    user = await UserModel.create(**data.model_dump())
    return user



async def get():
    return await UserModel.all()