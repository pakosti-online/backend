from app.models.user import User
from app.schemas.user import UserCreate



async def create_user(data: UserCreate) -> User:
    user = await User.create(**data.dict())
    return user


async def get_users():
    return await User.all()