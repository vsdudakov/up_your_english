from uuid import UUID

from pydantic import BaseModel


class MessageSchema(BaseModel):
    id: UUID
    name: str
    msg: str
    date: str


class PostMessageSchema(BaseModel):
    name: str
    msg: str
    date: str
