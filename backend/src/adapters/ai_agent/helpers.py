import asyncio
import typing as tp
from collections.abc import AsyncIterable

from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.language_models.llms import BaseLLM

from src.settings import settings


def get_llm(**kwargs: tp.Any) -> BaseLLM:
    kwargs["temperature"] = settings.TEMPERATURE
    kwargs["max_tokens"] = settings.MAX_TOKENS
    kwargs["frequency_penalty"] = settings.FREQUENCY_PENALTY
    kwargs["top_p"] = settings.TOP_P
    return OpenAI(**kwargs)


def get_prompt(
    resources: str,
    prompt_template: type[PromptTemplate],
) -> PromptTemplate:
    return prompt_template.from_template(resources)


def get_chain(
    llm: BaseLLM,
    prompt: PromptTemplate,
    output_parser: StrOutputParser,
) -> LLMChain:
    return LLMChain(llm=llm, prompt=prompt, output_parser=output_parser)


async def get_stream(
    chain: Chain,
    callback: AsyncIteratorCallbackHandler,
    config: tp.Any,
    multiple: bool = False,
    prompt_kwargs: dict[str, tp.Any] | None = None,
) -> AsyncIterable[str]:
    task = asyncio.create_task(chain.arun(**(prompt_kwargs or {}), config=config))

    async def stream_runner(chunk_size: int = 25) -> tp.Any:
        text = await chain.arun(prompt_kwargs or {})
        for i in range(0, len(text), chunk_size):
            if chunk := text[i : i + chunk_size]:
                yield chunk
            await asyncio.sleep(0.05)

    try:
        iterator = stream_runner() if multiple else callback.aiter()
        async for token in iterator:
            yield token
    finally:
        callback.done.set()
    await task
