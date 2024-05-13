import logging
import uuid

import orjson
from fastapi import WebSocket

from src.adapters.ai_agent.ai_agent import AIAgentAdapter
from src.adapters.queue import QueueAdapter
from src.core import Service
from src.schemas.chat import EMessageType, MessageSchema
from src.schemas.session import EFunctionality, EModel
from src.schemas.websocket import WsMessageSchema
from src.settings import settings

logger = logging.getLogger(__name__)


class WebsocketService(Service):
    ai_agent_adapter: AIAgentAdapter | None
    websocket: WebSocket | None

    async def accept(
        self,
        session_id: uuid.UUID,
        model: EModel,
        functionality: EFunctionality,
        websocket: WebSocket,
    ) -> None:
        self.ai_agent_adapter = self.bus.get_adapter(AIAgentAdapter)
        if self.ai_agent_adapter is None:
            raise RuntimeError("AIAgentAdapter is not found in bus")
        self.ai_agent_adapter.set_session(
            session_id=session_id,
            model=model,
            functionality=functionality,
        )
        self.websocket = websocket
        await self.websocket.accept()

    async def listen(self) -> None:
        if self.websocket is None or self.ai_agent_adapter is None:
            raise RuntimeError("WebSocket is not accepted. Run accept function")
        queue_adapter = self.bus.get_adapter(QueueAdapter)

        await self.ai_agent_adapter.welcome_message(self._send_message)
        while True:
            ws_message_dict = await queue_adapter.brpop(f"{settings.QUEUE_PREFIX}_{self.ai_agent_adapter.session_id}")
            if not ws_message_dict:
                continue
            ws_message = WsMessageSchema.model_validate(ws_message_dict)
            match ws_message.message_type:
                case EMessageType.TYPING:
                    pass
                case EMessageType.MESSAGE:
                    await self.ai_agent_adapter.process_message(ws_message.message, self._send_message)
                case _:
                    logger.warning("Unknown message type: %s", ws_message.message_type)

    async def close_ws(self) -> None:
        if self.websocket is None:
            raise RuntimeError("WebSocket is not accepted. Run accept function")
        await self.websocket.close()
        self.session_id = None
        self.websocket = None

    async def _send_message(self, message_type: EMessageType, message: MessageSchema) -> None:
        if self.websocket is None:
            raise RuntimeError("WebSocket is not accepted. Run accept function")
        response_message = WsMessageSchema(
            message_type=message_type,
            message=message,
        )
        try:
            await self.websocket.send_text(orjson.dumps(response_message.model_dump()).decode())
        except Exception:  # noqa: BLE001
            logger.warning("Failed to send message to WebSocket")
