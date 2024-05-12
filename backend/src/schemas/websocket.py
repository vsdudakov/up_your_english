from pydantic import BaseModel

from .chat import EMessageType, MessageSchema


class WsMessageSchema(BaseModel):
    message_type: EMessageType
    message: MessageSchema
