from fastapi import HTTPException, UploadFile, Depends
from fastapi.responses import FileResponse
from PIL import Image
import uuid
import os
import io

from .utils import validate_image_file
from app.models.user import UserModel, AvatarModel
from .auth import get_user
from app.schemas.avatars import UserAvatarOutDto, UserAvatarInDto, UserInDto


async def create_avatar_for_user(
    file: UploadFile, current_user: UserModel = Depends(get_user)
) -> UserAvatarOutDto:
    # Проверяем, что MIME-тип соответствует ожиданиям
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=404, detail="Разрешены только файлы JPG и PNG"
        )

    # Проверка, существует ли задача
    user = await UserModel.get_or_none(id=current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    file_bytes = await file.read()
    if not validate_image_file(file_bytes):
        raise HTTPException(
            status_code=404, detail="Неверный формат изображения"
        )

    # Открываем изображение с помощью Pillow
    try:
        image = Image.open(io.BytesIO(file_bytes))
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Ошибка обработки изображения: {str(e)}"
        )

    resampling_filter = Image.Resampling.LANCZOS

    # Сжимаем изображение до 256x256
    image = image.convert(
        "RGB"
    )  # Приводим изображение к RGB (на случай PNG с альфа-каналом)
    image = image.resize((256, 256), resampling_filter)

    # Генерируем уникальное имя файла с сохранением расширения
    unique_filename = f"{uuid.uuid4()}.jpg"  # Сохраняем как JPEG
    file_path = os.path.join("/backend/uploads/photoes", unique_filename)
    # Сохраняем сжатое изображение на диск
    try:
        image.save(file_path, "JPEG")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка сохранения сжатого изображения: {str(e)}",
        )

    # Удаляем старую аватарку, если она есть
    if user.avatar:
        try:
            old_avatar = await user.avatar
            os.remove(old_avatar.file_path)  # Удаляем файл с сервера
            await old_avatar.delete()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка удаления старой аватарки: {str(e)}",
            )

    avatar = await AvatarModel.create(file_path=file_path)

    # Обновляем аватарку пользователя
    user.avatar_id = avatar.id
    await user.save(update_fields=["avatar_id"])

    return UserAvatarOutDto.new(avatar)


async def delete_avatar(data: UserAvatarInDto) -> None:
    avatar = await AvatarModel.get_or_none(id=data.id)
    if not avatar:
        raise HTTPException(status_code=404, detail="Аватарка не найдена")

    if os.path.exists(avatar.file_path):
        try:
            os.remove(avatar.file_path)  # Удаляем файл с сервера
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка удаления файла: {str(e)}"
            )
    else:
        raise HTTPException(status_code=404, detail="Файл не найден на сервере")

    try:
        await avatar.delete()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка удаления аватара записи: {str(e)}"
        )

    return


async def create_url_by_user_id(data: UserInDto) -> FileResponse:
    avatar = await AvatarModel.get_or_none(id=data.id)
    if not avatar:
        raise HTTPException(status_code=404, detail="Аватарка не найдена")

    file_path = avatar.file_path

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден на сервере")

    # Определяем MIME-тип на основе расширения файла
    mime_type = (
        "image/jpeg" if file_path.endswith((".jpg", ".jpeg")) else "image/png"
    )

    return FileResponse(file_path, media_type=mime_type)
