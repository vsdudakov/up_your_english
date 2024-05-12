import uuid

from src.adapters.queue import QueueAdapter
from src.core import Service
from src.schemas.chat import EMessageType, MessageSchema
from src.schemas.websocket import WsMessageSchema
from src.settings import settings


class ChatService(Service):
    async def handle_message(self, session_id: uuid.UUID, message: MessageSchema) -> MessageSchema:
        queue_adapter: QueueAdapter = self.bus.get_adapter(QueueAdapter)
        ws_message = WsMessageSchema(
            message_type=EMessageType.MESSAGE,
            message=message,
        )
        await queue_adapter.lpush(
            f"{settings.QUEUE_PREFIX}_{session_id}",
            ws_message.model_dump(),
        )
        return message
