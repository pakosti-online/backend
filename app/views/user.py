from app.schemas.user import (
    CreateUserDto,
    UserDto,
    VerboseUserDto,
    UserTokensDto,
)

from fastapi.security import OAuth2PasswordRequestForm
import app.controllers.user as user_controller
from fastapi import APIRouter, Path, Depends

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=VerboseUserDto)
async def register(user: CreateUserDto):
    """Регистрация нового пользователя"""
    return await user_controller.create_user(user)


@router.post("/login", response_model=UserTokensDto)
async def login(input: OAuth2PasswordRequestForm = Depends()):
    """Вход пользователя. Генерирует Access/Refresh токены"""
    user, access, refresh = await user_controller.login(
        input.username, input.password
    )

    return UserTokensDto(
        user_data=VerboseUserDto.new(user),
        access_token=access,
        refresh_token=refresh,
    )


@router.post("/refresh", response_model=str)
async def refresh(token: str = Depends(user_controller.auth.OAUTH2_SCHEME)):
    """Обновление Access-токена. В заголовке Authorization необходимо указать Refresh-токен"""
    return await user_controller.refresh(token)


@router.get("", response_model=list[UserDto])
async def list_users():
    """Получение всех пользователей"""
    return await user_controller.get_users()


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int = Path(..., gt=0)):
    """Удаление пользователя по ID"""
    await user_controller.delete_user(user_id)


@router.get("/public/{user_id}", response_model=UserDto)
async def get_user(user_id: int = Path(..., gt=0)):
    """Возвращает публичную информацию о пользователе с данным user_id"""
    return await user_controller.get_user_by_id(user_id)


@router.get("/me")
async def get_user_verbose(user=Depends(user_controller.auth.get_user)):
    """Возвращает подробную информацию о текущем ауентифицированном пользователе"""
    return await user_controller.get_user_verbose(user.id)
