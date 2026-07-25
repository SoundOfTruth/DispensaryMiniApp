import asyncio
from uuid import uuid4

import pytest
from pydantic import BaseModel

from src.cache.manager import CacheManager


class SchemaForTest(BaseModel):
    name: str


class NestedSchemaForTest(BaseModel):
    obj: SchemaForTest


data_to_cache = [
    "string",
    100,
    100.1,
    None,
    True,
    {"cache": True},
    SchemaForTest(name="test"),
    [SchemaForTest(name="test"), SchemaForTest(name="test")],
    NestedSchemaForTest(obj=SchemaForTest(name="test")),
    [
        NestedSchemaForTest(obj=SchemaForTest(name="test")),
        NestedSchemaForTest(obj=SchemaForTest(name="test")),
    ],
    ["string", "other_string"],
    set([1, 2, 3]),
    (1, 2, 3),
]


@pytest.mark.usefixtures("init_cache")
class TestCache:
    async def test_cache_save_decorator(self):
        args = (1, 2, 3)
        kwargs = {"a": 1, "b": 2, "c": 3}
        cm = CacheManager(uuid4().hex)
        payload = []

        def task(*args, **kwargs):
            copy = payload.copy()
            payload.extend([*args])
            payload.extend([kwargs[key] for key in kwargs])
            return copy

        func = cm.use(task, ttl=20)

        no_args_ret = await func()
        payload.append(1)
        args_ret = await func(*args)
        kwargs_ret = await func(**kwargs)
        args_kwargs_ret = await func(*args, **kwargs)

        assert no_args_ret != task()
        assert no_args_ret == await func()
        assert args_ret != task(*args)
        assert args_ret == await func(*args)
        assert kwargs_ret != task(**kwargs)
        assert kwargs_ret == await func(**kwargs)
        assert args_kwargs_ret != task(*args, **kwargs)
        assert args_kwargs_ret == await func(*args, **kwargs)
        assert len(args_kwargs_ret) > len(kwargs_ret) > len(args_ret) > len(no_args_ret)

    async def test_cache_save_decorator_ttl(self):
        fake_db = {"cache": True}

        def task():
            return fake_db["cache"]

        cm = CacheManager(uuid4().hex)
        cache_func = cm.use(task, ttl=1)
        await cache_func()
        cached = await cache_func()
        fake_db["cache"] = False
        await asyncio.sleep(1)
        assert cached
        assert not await cache_func()

    async def test_cache_expire_decorator(self):
        fake_db = {"cache": True}

        def task():
            return fake_db["cache"]

        cm = CacheManager(uuid4().hex)
        cache_func = cm.use(task, ttl=60)
        expire_func = cm.expire(task)
        await cache_func()
        cached = await cache_func()
        fake_db["cache"] = False
        await expire_func()
        assert cached
        assert not await cache_func()

    @pytest.mark.parametrize("data", data_to_cache)
    async def test_cache_param_types(self, data):
        cm = CacheManager(uuid4().hex)

        @cm.use(ttl=60)
        def task(data):
            return data

        await task(data)
        cached = await task(data)
        data_type = type(data)
        if data_type in {set, tuple, list}:
            valid_data = [
                item.model_dump(mode="json") if isinstance(item, BaseModel) else item
                for item in data
            ]
            assert cached == valid_data
        elif isinstance(data, BaseModel):
            assert cached == data.model_dump(mode="json")
        else:
            assert cached == data
