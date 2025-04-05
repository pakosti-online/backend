from fastapi import APIRouter
from . import user, transaction, websocket

api_router = APIRouter()

api_router.include_router(user.router)
api_router.include_router(transaction.router)
api_router.include_router(websocket.router)
