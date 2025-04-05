from fastapi import FastAPI
from app.db import init_db
from app.views.user_views import router as user_router
from app.views.transaction_views import router as transaction_router


def create_application():
    app = FastAPI(title="Pakosti Online", docs_url="/swagger")
    app.include_router(user_router)
    app.include_router(transaction_router)

    init_db(app)

    return app


app = create_application()
