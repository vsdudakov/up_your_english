from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class EMessageType(StrEnum):
    WELCOME = "WELCOME"
    MESSAGE = "MESSAGE"
    TYPING = "TYPING"


class MessageSchema(BaseModel):
    id: UUID
    user_name: str
    message: str
    timestamp: int
