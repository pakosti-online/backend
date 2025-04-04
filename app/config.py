# пока скопипастил из предыдущих реп, мейби удалю
# from pydantic import BaseSettings

# class Settings(BaseSettings):
#     postgres_username: str
#     postgres_password: str
#     postgres_host: str
#     postgres_port: int
#     postgres_dbname: str
#     jwt_secret: str


# settings = Settings()


# postgres_url = "postgres://{username}:{password}@{host}:{port}/{dbname}".format(
#         username=settings.postgres_username,
#         password=settings.postgres_password,
#         host=settings.postgres_host,
#         port=settings.postgres_port,
#         dbname=settings.postgres_dbname,
# )



TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["app.models.user", "aerich.models"],
            "default_connection": "default",
        },
    },
}
