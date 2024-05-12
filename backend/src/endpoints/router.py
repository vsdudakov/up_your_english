from fastapi import APIRouter

from src.endpoints.chat import router as chat_router
from src.endpoints.websocket import router as websocket_router

api_router = APIRouter(
    prefix="/api",
)

api_router.include_router(chat_router)
api_router.include_router(websocket_router)
