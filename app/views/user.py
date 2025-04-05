from app.schemas.user import (
    CreateUserDto,
    UserDto,
    VerboseUserDto,
    UserTokensDto,
    UserEditPublicDto,
)
from app.schemas.avatars import UserAvatarOutDto, UserAvatarInDto

from fastapi.security import OAuth2PasswordRequestForm
import app.controllers.user as user_controller
from fastapi import APIRouter, Path, Depends, UploadFile


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


@router.get("/public/{user_id}", response_model=UserDto)
async def get_user(user_id: int = Path(..., gt=0)):
    """Возвращает публичную информацию о пользователе с данным user_id"""
    return await user_controller.get_user_by_id(user_id)


@router.get("/me")
async def get_user_verbose(user=Depends(user_controller.auth.get_user)):
    """Возвращает подробную информацию о текущем аутентифицированном пользователе"""
    return await user_controller.get_user_verbose(user.id)


@router.patch("/edit", response_model=VerboseUserDto)
async def edit_public_info(
    update_info: UserEditPublicDto, user=Depends(user_controller.auth.get_user)
):
    """Позволяет изменять публичные данные о пользователе"""
    await user_controller.update_public_info(user, update_info)
    return user


@router.post("/avatar", response_model=UserAvatarOutDto)
async def create_avatar_for_user(
    file: UploadFile, user=Depends(user_controller.auth.get_user)
):
    """Создание аватарки для пользователя, если такая есть то предыдущая удаляется"""
    return await user_controller.avatars.create_avatar_for_user(file, user)
