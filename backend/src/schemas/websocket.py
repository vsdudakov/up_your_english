import typing as tp
from enum import StrEnum

from pydantic import BaseModel


class EWsMessageType(StrEnum):
    MESSAGE = "MESSAGE"
    TYPING = "TYPING"


class WsMessageSchema(BaseModel):
    message_type: EWsMessageType
    payload: dict[str, tp.Any]
