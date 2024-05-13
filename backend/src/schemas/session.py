import uuid
from enum import StrEnum

from pydantic import BaseModel


class EModel(StrEnum):
    DAVINCI = "davinci-002"
    TEXT_DAVINCI = "text-davinci-003"
    BABBAGE = "babbage-002"
    ADA = "text-ada-001"
    GPT3 = "gpt-3.5-turbo-instruct"


class EFunctionality(StrEnum):
    WRITE_PROPERLY = "write-properly"
    WRITE_THE_SAME_GRAMMAR_FIXED = "write-the-same-grammar-fixed"
    SUMMARIZE = "summarize"


class CreateSessionSchema(BaseModel):
    model: EModel
    functionality: EFunctionality


class SessionSchema(BaseModel):
    session_id: uuid.UUID
    model: EModel
    functionality: EFunctionality
