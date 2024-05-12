import uuid
from enum import StrEnum

from pydantic import BaseModel


class EModel(StrEnum):
    DAVINCI = "davinci-002"
    TEXT_DAVINCI = "text-davinci-003"
    BABBAGE = "babbage-002"
    ADA = "text-ada-001"
    GPT3 = "gpt-3.5-turbo-instruct"


class ETopic(StrEnum):
    GRAMMAR = "GRAMMAR"
    STYLE = "STYLE"
    SUMMARIZATION = "SUMMARIZATION"


class CreateSessionSchema(BaseModel):
    model: EModel
    topic: ETopic


class SessionSchema(BaseModel):
    session_id: uuid.UUID
    model: EModel
    topic: ETopic
