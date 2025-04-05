from app.views import api_router
from fastapi import FastAPI
from app.db import init_db


def create_application():
    app = FastAPI(title="Pakosti Online", docs_url="/swagger")
    app.include_router(api_router)

    init_db(app)

    return app


app = create_application()
