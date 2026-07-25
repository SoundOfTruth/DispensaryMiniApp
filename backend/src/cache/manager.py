import json
from functools import wraps
from inspect import iscoroutinefunction
from typing import Any, Awaitable, Callable, Sequence, overload

from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from redis.asyncio import Redis

from src.cache.backend import CacheBackend
from src.cache.key_builder import KeyBuilder
from src.services.exceptions import NotFoundError

type Allowed = BaseModel | str | int | float | dict[str, Any]
type Cacheable = Allowed | Sequence[Allowed]
type WrappedFunc[T: Cacheable] = Callable[..., Awaitable[T]]


async def execute_task(task: Callable, *args, **kwargs):
    if iscoroutinefunction(task):
        return await task(*args, **kwargs)
    else:
        return await run_in_threadpool(task, *args, **kwargs)


def dump(res: Cacheable) -> str:
    if isinstance(res, BaseModel):
        return res.model_dump_json()
    if isinstance(res, list) or isinstance(res, set) or isinstance(res, tuple):
        return json.dumps(
            [
                item.model_dump(mode="json") if isinstance(item, BaseModel) else item
                for item in res
            ]
        )
    return json.dumps(res)


class CacheManager:
    backend: CacheBackend | None = None
    base_prefix: str = "cache"
    fall_count: int = 0

    @classmethod
    def init(cls, client: Redis, prefix: str = "cache") -> None:
        cls.backend = CacheBackend(client)
        cls.base_prefix = prefix

    def __init__(self, prefix: str) -> None:
        self._prefix: str = prefix

    @property
    def prefix(self):
        return f"{self.base_prefix}:{self._prefix}"

    @overload
    def use[T: Cacheable](
        self,
        func: Callable[..., T | Awaitable[T]],
        ttl: int = 120,
    ) -> WrappedFunc[T]: ...

    @overload
    def use[T: Cacheable](
        self,
        func: None = None,
        ttl: int = 120,
    ) -> Callable[[Callable[..., T | Awaitable[T]]], WrappedFunc[T]]: ...

    def use[T: Cacheable](
        self,
        func: Callable[..., T | Awaitable[T]] | None = None,
        ttl: int = 120,
    ) -> WrappedFunc[T] | Callable[[Callable[..., T | Awaitable[T]]], WrappedFunc[T]]:
        def inner(func: Callable[..., T | Awaitable[T]]) -> WrappedFunc[T]:
            @wraps(func)
            async def wrapper(*args, **kwargs) -> T:
                if self.backend is None:
                    return await execute_task(func, *args, **kwargs)

                key = KeyBuilder(self.prefix, func, *args, **kwargs).key
                cached = await self.backend.get(key)
                if cached is not None:
                    if cached == "__404__":
                        raise NotFoundError
                    return json.loads(cached)
                try:
                    res = await execute_task(func, *args, **kwargs)
                    await self.backend.save(key, dump(res), ttl)
                    return res
                except NotFoundError as ex:
                    await self.backend.save(key, "__404__", ttl)
                    raise ex

            return wrapper

        if func is not None:
            return inner(func)
        else:
            return inner

    def expire(self, func: Callable | None = None) -> Callable:
        def inner(func: Callable) -> Callable[..., Awaitable]:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                res = await execute_task(func, *args, **kwargs)
                if self.backend is None:
                    return res
                key = KeyBuilder(self.prefix, func, *args, **kwargs)
                await self.backend.expire(key)
                return res

            return wrapper

        if func is not None:
            return inner(func)
        return inner
