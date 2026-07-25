from redis.asyncio import Redis
from redis.exceptions import ConnectionError, TimeoutError

from src.cache.key_builder import KeyBuilder


class CacheBackend:
    def __init__(self, client: Redis) -> None:
        self.client: Redis = client
        self.fall_count: int = 0
        self.check_count = 0

    async def ping(self) -> None:
        self.check_count += 1
        if self.fall_count >= 3 and self.check_count % 100 == 0:
            try:
                ping = await self.client.ping()
            except (ConnectionError, TimeoutError):
                pass
            else:
                if ping:
                    self.fall_count = 0
                    self.check_count = 0

    def is_alive(self) -> bool:
        return self.fall_count < 3

    def on_error(self):
        self.fall_count += 1

    async def get(self, key: str) -> bytes | str | None:
        if not self.is_alive():
            await self.ping()
            return
        try:
            return await self.client.get(key)
        except (ConnectionError, TimeoutError):
            self.on_error()

    async def save(self, key: str, val, ttl: int) -> None:
        if not self.is_alive():
            await self.ping()
            return
        try:
            await self.client.set(key, val, ex=ttl)
        except (ConnectionError, TimeoutError):
            self.on_error()

    async def expire(self, builder: KeyBuilder):
        if not self.is_alive():
            await self.ping()
            return
        keys = set()
        if builder.id:
            keys.add(builder.key)
        prefix = f"{builder.prefix}:list*"
        try:
            async for key in self.client.scan_iter(prefix):
                keys.add(key)
        except (ConnectionError, TimeoutError):
            self.on_error()
        try:
            await self.client.unlink(*keys)
        except (ConnectionError, TimeoutError):
            self.on_error()
