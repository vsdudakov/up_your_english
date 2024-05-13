import uuid

from fastapi import APIRouter, Depends, WebSocket

from src.endpoints.deps import get_ws_functionality, get_ws_model, get_ws_service, get_ws_session_id, get_ws_style
from src.schemas.session import EFunctionality, EModel
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
    functionality: EFunctionality = Depends(get_ws_functionality),
    style: str | None = Depends(get_ws_style),
    websocket_service: WebsocketService = Depends(get_ws_service(WebsocketService)),
) -> None:
    try:
        await websocket_service.accept(
            session_id,
            model,
            functionality,
            style,
            websocket,
        )
        await websocket_service.listen()
    finally:
        await websocket_service.close_ws()
