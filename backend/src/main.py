from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.ai_agent import AIAgentAdapter
from src.adapters.queue import QueueAdapter
from src.core import Bus
from src.endpoints.router import api_router
from src.settings import settings

bus = Bus()

bus.register_adapter(QueueAdapter(settings.REDIS_DSN))
bus.register_adapter(AIAgentAdapter())


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Up bus
    bus: Bus = app.extra["bus"]
    await bus.up()
    if not await bus.healthcheck():
        raise Exception("Bus is not healthy")
    # Run app
    yield
    # Down bus
    await bus.down()


root_asgi_app = FastAPI(
    title="Backend API",
    description="Backend API",
    version="0.1.0",
    lifespan=lifespan,
    bus=bus,
)

root_asgi_app.include_router(api_router)

root_asgi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
