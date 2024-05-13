from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_DSN: str = "redis://localhost:6379/0"
    QUEUE_PREFIX: str = "stream"
    OPENAI_API_KEY: str


settings = Settings()  # type: ignore [call-arg]
