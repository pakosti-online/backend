from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserOut
from app.controllers import user_controller


router = APIRouter(prefix="/users", tags=["Users"])



@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate):
    return await user_controller.create_user(user)

@router.get("/", response_model=list[UserOut])
async def list_users():
    return await user_controller.get_users()