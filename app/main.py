from fastapi.middleware.cors import CORSMiddleware
from app.views import api_router
from fastapi import FastAPI
from app.db import init_db
from app.db_seed import create_categories, create_educate


def create_application():
    app = FastAPI(title="Pakosti Online", docs_url="/swagger")

    # we do real PAKOSTI here
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_db(app)
    app.include_router(api_router)

    return app


app = create_application()


@app.on_event("startup")
async def startup_event():
    await create_categories()
    await create_educate()
