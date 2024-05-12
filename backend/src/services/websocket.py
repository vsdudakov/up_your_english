import asyncio
import logging
import typing as tp
import uuid

import orjson
from fastapi import WebSocket

from src.adapters.ai_agent import AIAgentAdapter
from src.adapters.queue import QueueAdapter
from src.core import Service
from src.schemas.chat import MessageSchema
from src.schemas.websocket import EWsMessageType, WsMessageSchema
from src.settings import settings

logger = logging.getLogger(__name__)


class WebsocketService(Service):
    session_id: uuid.UUID | None
    websocket: WebSocket | None

    async def accept(self, session_id: uuid.UUID, websocket: WebSocket) -> None:
        self.session_id = session_id
        self.websocket = websocket
        await self.websocket.accept()

    async def listen(self) -> None:
        if self.session_id is None or self.websocket is None:
            raise RuntimeError("WebSocket is not accepted. Run accept function")
        queue_adapter = self.bus.get_adapter(QueueAdapter)
        while True:
            try:
                ws_message_dict = await queue_adapter.brpop(f"{settings.QUEUE_PREFIX}_{self.session_id}")
                if not ws_message_dict:
                    continue
                await self.handle_ws_message(ws_message_dict)
                await asyncio.sleep(0.5)
            except Exception as e:
                logger.exception("Error in listen loop: %s", e)

    async def close_ws(self) -> None:
        if self.session_id is None or self.websocket is None:
            raise RuntimeError("WebSocket is not accepted. Run accept function")

        await self.websocket.close()
        self.session_id = None
        self.websocket = None

    async def handle_ws_message(self, ws_message_dict: dict[str, tp.Any]) -> None:
        if self.session_id is None or self.websocket is None:
            raise RuntimeError("WebSocket is not accepted. Run accept function")

        ai_agent_adapter: AIAgentAdapter = self.bus.get_adapter(AIAgentAdapter)
        ws_message = WsMessageSchema.model_validate(ws_message_dict)

        match ws_message.message_type:
            case EWsMessageType.MESSAGE:
                message = MessageSchema.model_validate(ws_message.payload)

                async def response_callback(message_type: EWsMessageType, payload: dict[str, tp.Any]) -> None:
                    response_message = WsMessageSchema(
                        message_type=message_type,
                        payload=payload,
                    )
                    await self.send(response_message.model_dump())

                await ai_agent_adapter.process_message(message, response_callback)
            case _:
                logger.warning("Unknown message type: %s", ws_message.message_type)

    async def send(self, payload: dict[str, tp.Any]) -> None:
        if self.websocket is None:
            raise RuntimeError("WebSocket is not accepted. Run accept function")
        await self.websocket.send_json(orjson.loads(orjson.dumps(payload)))
