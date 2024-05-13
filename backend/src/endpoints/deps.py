import uuid
from collections.abc import Callable

from fastapi import Depends, HTTPException, Request, WebSocket, WebSocketDisconnect

from src.core import Bus, Service
from src.schemas.session import EFunctionality, EModel


def get_bus(request: Request) -> Bus:
    return request.app.extra["bus"]


def get_service(service_cls: type[Service]) -> Callable[[Bus], Service]:
    def wrapper(bus: Bus = Depends(get_bus)) -> Service:
        return service_cls(bus)

    return wrapper


def get_session_id(request: Request) -> uuid.UUID:
    session_id: str | None = request.cookies.get("session_id")
    if session_id is None:
        raise HTTPException(status_code=401, detail="session_id is required")
    return uuid.UUID(session_id)


def get_ws_bus(websocket: WebSocket) -> Bus:
    return websocket.app.extra["bus"]


def get_ws_service(service_cls: type[Service]) -> Callable[[Bus], Service]:
    def wrapper(bus: Bus = Depends(get_ws_bus)) -> Service:
        return service_cls(bus)

    return wrapper


def get_ws_session_id(websocket: WebSocket) -> uuid.UUID:
    session_id: str | None = websocket.cookies.get("session_id")
    if session_id is None:
        raise WebSocketDisconnect(code=401, reason="session_id is required")
    return uuid.UUID(session_id)


def get_ws_model(websocket: WebSocket) -> EModel:
    model: str | None = websocket.cookies.get("model")
    if model is None:
        raise WebSocketDisconnect(code=401, reason="session_id is required")
    return EModel(model)


def get_ws_functionality(websocket: WebSocket) -> EFunctionality:
    functionality: str | None = websocket.cookies.get("functionality")
    if functionality is None:
        raise WebSocketDisconnect(code=401, reason="session_id is required")
    return EFunctionality(functionality)
