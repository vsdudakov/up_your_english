from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_DSN: str = "redis://localhost:6379/0"
    QUEUE_PREFIX: str = "stream"
    OPENAI_API_KEY: str
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2000
    FREQUENCY_PENALTY: float = 0.0
    TOP_P: float = 1.0


settings = Settings()  # type: ignore [call-arg]
