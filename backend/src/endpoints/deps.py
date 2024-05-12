import uuid
from collections.abc import Callable

from fastapi import Depends, HTTPException, Request

from src.core import Bus, Service


def get_bus(request: Request) -> Bus:
    return request.app.extra["bus"]


def get_service(service_cls: type[Service]) -> Callable[[Bus], Service]:
    def wrapper(bus: Bus = Depends(get_bus)) -> Service:
        return service_cls(bus)

    return wrapper


def get_session_id(request: Request) -> uuid.UUID:
    session_id: str | None = request.headers.get("Session-ID")
    if session_id is None:
        raise HTTPException(status_code=401, detail="Session-ID header is required")
    return uuid.UUID(session_id)
