import asyncio
import typing as tp

from src.core import BusAdapter
from src.schemas.chat import MessageSchema
from src.schemas.websocket import EWsMessageType


class AIAgentAdapter(BusAdapter):
    async def up(self) -> None:
        pass

    async def healthcheck(self) -> bool:
        return True

    async def down(self) -> None:
        pass

    async def process_message(
        self,
        message: MessageSchema,
        response_callback: tp.Any,
    ) -> None:
        # echo
        await response_callback(
            EWsMessageType.TYPING,
            {
                "name": "AI Agent",
                "msg": "Typing...",
            },
        )
        message.name = "AI Agent"
        await asyncio.sleep(2)
        await response_callback(
            EWsMessageType.MESSAGE,
            {
                "name": "AI Agent",
                "msg": f"Echo: {message.msg}",
                "date": message.date,
            },
        )
