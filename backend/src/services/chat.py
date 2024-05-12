import uuid

from src.adapters.queue import QueueAdapter
from src.core import Service
from src.schemas.chat import MessageSchema, PostMessageSchema
from src.schemas.websocket import EWsMessageType, WsMessageSchema
from src.settings import settings


class ChatService(Service):
    async def handle_message(self, session_id: uuid.UUID, payload: PostMessageSchema) -> MessageSchema:
        queue_adapter: QueueAdapter = self.bus.get_adapter(QueueAdapter)
        response = MessageSchema(
            id=uuid.uuid4(),
            name=payload.name,
            msg=payload.msg,
            date=payload.date,
        )
        ws_message = WsMessageSchema(
            message_type=EWsMessageType.MESSAGE,
            payload=response.model_dump(),
        )
        await queue_adapter.lpush(
            f"{settings.QUEUE_PREFIX}_{session_id}",
            ws_message.model_dump(),
        )
        return response
