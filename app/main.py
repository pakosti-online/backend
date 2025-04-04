# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from tortoise.contrib.fastapi import register_tortoise
# # import asyncio

# from app.config import settings
# from app.controllers import user_router

# def create_app() -> FastAPI:
#     application = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

#     application.include_router(user_router, prefix="", tags = ['User\'s routes'])


#     application.add_middleware(
#         CORSMiddleware,
#         allow_origins=["http://localhost"],  # Подгонять относительно данных из .env.example или подобного так как это влияет (ссылка на домен/фронт)
#         allow_credentials=True,  # Разрешить передачу кук
#         allow_methods=["*"],  # Разрешить все методы
#         allow_headers=["*"],  # Разрешить все заголовки
#     )

#     postgres_url = "postgres://{username}:{password}@{host}:{port}/{dbname}".format(
#         username=settings.postgres_username,
#         password=settings.postgres_password,
#         host=settings.postgres_host,
#         port=settings.postgres_port,
#         dbname=settings.postgres_dbname,
#     )

#     register_tortoise(
#         application,
#         db_url=postgres_url,
#         modules={"models": ["app.models.user_model"]}, # регистрация моделей
#         generate_schemas=True,
#         add_exception_handlers=True,
#     )

#     return application



# app = create_app()


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