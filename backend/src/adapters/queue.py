import typing as tp

import orjson
import redis.asyncio as redis

from src.core import BusAdapter


class QueueAdapter(BusAdapter):
    redis: redis.Redis | None
    redis_dsn: str

    def __init__(self, redis_dsn: str) -> None:
        self.redis_dsn = redis_dsn
        self.redis = None

    async def up(self) -> None:
        self.redis = await redis.from_url("redis://localhost")

    async def healthcheck(self) -> bool:
        if not self.redis:
            return False
        try:
            await self.redis.ping()
            return True
        except redis.RedisError:
            return False

    async def down(self) -> None:
        if not self.redis:
            return
        await self.redis.close()

    async def brpop(self, queue_name: str) -> dict[str, tp.Any] | None:
        if not self.redis:
            raise RuntimeError("QueueAdapter is not up yet.")
        _, data = await self.redis.brpop([queue_name])  # type: ignore [misc]
        if not data:
            return None
        try:
            return orjson.loads(data)
        except orjson.JSONDecodeError:
            return None

    async def lpush(self, queue_name: str, message: dict[str, tp.Any]) -> bool:
        if not self.redis:
            raise RuntimeError("QueueAdapter is not up yet.")
        try:
            await self.redis.lpush(queue_name, orjson.dumps(message))  # type: ignore [misc]
            return True
        except orjson.JSONEncodeError:
            return False
