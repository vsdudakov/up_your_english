import typing as tp
import uuid
from time import time

from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.callbacks.tracers.run_collector import RunCollectorCallbackHandler
from langchain.chains import SimpleSequentialChain
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableConfig

import src.adapters.ai_agent.prompts as tmp
from src.core import BusAdapter
from src.schemas.chat import EMessageType, MessageSchema
from src.schemas.session import EFunctionality, EModel

from .helpers import get_chain, get_llm, get_prompt, get_stream


class AIAgentAdapter(BusAdapter):
    session_id: uuid.UUID | None
    model: EModel | None
    functionality: EFunctionality | None
    style: str | None

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
        functionality: EFunctionality,
        style: str | None = None,
    ) -> None:
        self.session_id = session_id
        self.model = model
        self.functionality = functionality
        self.style = style

    async def welcome_message(
        self,
        send_message: tp.Any,
    ) -> None:
        if self.model is None or self.functionality is None:
            raise RuntimeError("Session is not set yet.")
        message_id = uuid.uuid4()
        model = self.model.value.lower()
        functionality = self.functionality.value.lower()
        message = "Welcome to English class room."
        if self.model:
            message += f" Your model is {model}."
        if self.functionality:
            message += f" Your functionality is {functionality}."
        if self.style:
            message += f" Your style is {self.style}."
        message += " Please provide your message below."
        await send_message(
            EMessageType.WELCOME,
            MessageSchema(
                id=message_id,
                user_name=self.user_name,
                message=message,
                timestamp=int(time() * 1000),
            ),
        )

    async def process_message(
        self,
        message: MessageSchema,
        send_message: tp.Any,
    ) -> None:
        if self.functionality is None:
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
        match self.functionality:
            case EFunctionality.WRITE_THE_SAME_GRAMMAR_FIXED:
                await self._write_the_same_grammar_fixed(message_id, message, send_message)
            case EFunctionality.WRITE_PROPERLY:
                await self._write_properly(message_id, message, send_message)
            case EFunctionality.SUMMARIZE:
                await self._summarize(message_id, message, send_message)
            case _:
                raise RuntimeError("Unknown functionality")

    async def _write_the_same_grammar_fixed(
        self,
        message_id: uuid.UUID,
        message: MessageSchema,
        send_message: tp.Any,
    ) -> None:
        run_collector = RunCollectorCallbackHandler()
        runnable_config = RunnableConfig(callbacks=[run_collector])
        callback = AsyncIteratorCallbackHandler()
        llm_params = {
            "model": self.model,
            "streaming": True,
            "callbacks": [callback],
        }

        llm = get_llm(**llm_params)
        prompt = get_prompt(
            resources=tmp.grammar_template,
            prompt_template=PromptTemplate,
        )
        chain = get_chain(
            llm=llm,
            prompt=prompt,
            output_parser=StrOutputParser(),
        )
        async for chunk in get_stream(
            chain=chain,
            callback=callback,
            config=runnable_config,
            prompt_kwargs={
                "input": message.message,
            },
        ):
            await send_message(
                EMessageType.MESSAGE_CHUNK,
                MessageSchema(
                    id=message_id,
                    user_name=self.user_name,
                    message=chunk,
                    timestamp=int(time() * 1000),
                ),
            )

    async def _write_properly(
        self,
        message_id: uuid.UUID,
        message: MessageSchema,
        send_message: tp.Any,
    ) -> None:
        run_collector = RunCollectorCallbackHandler()
        runnable_config = RunnableConfig(callbacks=[run_collector])
        callback = AsyncIteratorCallbackHandler()
        llm_params = {
            "model": self.model,
            "streaming": True,
            "callbacks": [callback],
        }

        llm = get_llm(**llm_params)
        grammar_prompt = get_prompt(
            resources=tmp.grammar_template,
            prompt_template=PromptTemplate,
        )
        grammar_chain = get_chain(
            llm=llm,
            prompt=grammar_prompt,
            output_parser=StrOutputParser(),
        )
        style_template = tmp.style_template.replace(
            "{style}", self.style or "Let yourself get inspired by the randomness of the AI."
        )
        style_prompt = get_prompt(
            resources=style_template,
            prompt_template=PromptTemplate,
        )
        style_chain = get_chain(
            llm=llm,
            prompt=style_prompt,
            output_parser=StrOutputParser(),
        )
        chain = SimpleSequentialChain(
            chains=[style_chain, grammar_chain],
        )
        async for chunk in get_stream(
            chain=chain,
            callback=callback,
            config=runnable_config,
            prompt_kwargs={
                "input": message.message,
            },
        ):
            await send_message(
                EMessageType.MESSAGE_CHUNK,
                MessageSchema(
                    id=message_id,
                    user_name=self.user_name,
                    message=chunk,
                    timestamp=int(time() * 1000),
                ),
            )

    async def _summarize(
        self,
        message_id: uuid.UUID,
        message: MessageSchema,
        send_message: tp.Any,
    ) -> None:
        run_collector = RunCollectorCallbackHandler()
        runnable_config = RunnableConfig(callbacks=[run_collector])
        callback = AsyncIteratorCallbackHandler()
        llm_params = {
            "model": self.model,
            "streaming": True,
            "callbacks": [callback],
        }

        llm = get_llm(**llm_params)
        prompt = get_prompt(
            resources=tmp.summarization_default_template,
            prompt_template=PromptTemplate,
        )
        chain = get_chain(
            llm=llm,
            prompt=prompt,
            output_parser=StrOutputParser(),
        )
        async for chunk in get_stream(
            chain=chain,
            callback=callback,
            config=runnable_config,
            prompt_kwargs={
                "input": message.message,
            },
        ):
            await send_message(
                EMessageType.MESSAGE_CHUNK,
                MessageSchema(
                    id=message_id,
                    user_name=self.user_name,
                    message=chunk,
                    timestamp=int(time() * 1000),
                ),
            )
