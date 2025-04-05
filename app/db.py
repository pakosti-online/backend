from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from os import environ

TORTOISE_ORM = {
    "connections": {"default": environ["DATABASE_URL"]},
    "apps": {
        "models": {
            "models": ["app.models.user", "app.models.transaction", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    Tortoise.init_models(["app.models.user", "app.models.transaction"], "models")
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        modules={"models": ["app.models.user", "app.models.transaction"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
