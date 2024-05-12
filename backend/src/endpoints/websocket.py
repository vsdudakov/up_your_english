import uuid

from fastapi import APIRouter, HTTPException, WebSocket

from src.services.websocket import WebsocketService

router = APIRouter(
    prefix="/ws",
    tags=["ws"],
)


@router.websocket("")
async def websocket(
    websocket: WebSocket,
) -> None:
    session_id = websocket.query_params.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    bus = websocket.app.extra["bus"]
    websocket_service = WebsocketService(bus)
    await websocket_service.accept(
        uuid.UUID(session_id),
        websocket,
    )
    await websocket_service.listen()
    await websocket_service.close_ws()
