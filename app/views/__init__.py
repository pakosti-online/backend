from fastapi import APIRouter
from . import user, transaction, websocket, analytics, finances_ed

api_router = APIRouter()

api_router.include_router(user.router)
api_router.include_router(transaction.router)
api_router.include_router(websocket.router)
api_router.include_router(analytics.router)
api_router.include_router(finances_ed.router)
