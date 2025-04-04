from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.config import TORTOISE_ORM
from app.views.user_view import router as user_router


def create_application():

    app = FastAPI(title="FastAPI + TortoiseORM + MVC")

    app.include_router(user_router)

    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,  # Используем миграции через Aerich
        add_exception_handlers=True,
    )

    return app

app = create_application()