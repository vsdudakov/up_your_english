import asyncio
import typing as tp
import uuid
from time import time

from src.core import BusAdapter
from src.schemas.chat import EMessageType, MessageSchema
from src.schemas.session import EModel, ETopic


class AIAgentAdapter(BusAdapter):
    session_id: uuid.UUID | None
    model: EModel | None
    topic: ETopic | None

    user_name = "English Teacher"

    async def up(self) -> None:
        pass

    async def healthcheck(self) -> bool:
        return True

    async def down(self) -> None:
        pass

    def set_session(
        self,
        session_id: uuid.UUID,
        model: EModel,
        topic: ETopic,
    ) -> None:
        self.session_id = session_id
        self.model = model
        self.topic = topic

    async def welcome_message(
        self,
        send_message: tp.Any,
    ) -> None:
        if any(v is None for v in (self.session_id, self.model, self.topic)):
            raise RuntimeError("Session is not set yet.")
        message_id = uuid.uuid4()
        model = self.model.value.lower() if self.model else "None"
        topic = self.topic.value.lower() if self.topic else "None"
        await send_message(
            EMessageType.WELCOME,
            MessageSchema(
                id=message_id,
                user_name=self.user_name,
                message=f"""
                    Welcome to English class room. Your model is {model}. Your topic is {topic}. Please provide your messages below.
                """,
                timestamp=int(time() * 1000),
            ),
        )

    async def process_message(
        self,
        message: MessageSchema,
        send_message: tp.Any,
    ) -> None:
        if any(v is None for v in (self.session_id, self.model, self.topic)):
            raise RuntimeError("Session is not set yet.")
        message_id = uuid.uuid4()
        await send_message(
            EMessageType.TYPING,
            MessageSchema(
                id=message_id,
                user_name=self.user_name,
                message="Typing...",
                timestamp=int(time() * 1000),
            ),
        )
        await asyncio.sleep(2)
        await send_message(
            EMessageType.MESSAGE,
            MessageSchema(
                id=message_id,
                user_name=self.user_name,
                message=f"Echo {message.message}",
                timestamp=int(time() * 1000),
            ),
        )
