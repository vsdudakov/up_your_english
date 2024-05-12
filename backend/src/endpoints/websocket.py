import uuid

from fastapi import APIRouter, Depends, WebSocket

from src.endpoints.deps import get_ws_model, get_ws_service, get_ws_session_id, get_ws_topic
from src.schemas.session import EModel, ETopic
from src.services.websocket import WebsocketService

router = APIRouter(
    prefix="/ws",
    tags=["ws"],
)


@router.websocket("")
async def websocket(
    websocket: WebSocket,
    session_id: uuid.UUID = Depends(get_ws_session_id),
    model: EModel = Depends(get_ws_model),
    topic: ETopic = Depends(get_ws_topic),
    websocket_service: WebsocketService = Depends(get_ws_service(WebsocketService)),
) -> None:
    try:
        await websocket_service.accept(
            session_id,
            model,
            topic,
            websocket,
        )
        await websocket_service.listen()
    finally:
        await websocket_service.close_ws()
