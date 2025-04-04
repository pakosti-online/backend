


TORTOISE_ORM = {
    "connections": {
        "default": "postgres://postgres:password@localhost:5432/mydatabase"
    },
    "apps": {
        "models": {
            "models": ["app.models.user", "aerich.models"],
            "default_connection": "default",
        },
    },
}