from copy import deepcopy
from uuid import uuid4

import pytest
from pydantic import BaseModel

from src.cache.key_builder import KeyBuilder


class SchemaForTest(BaseModel):
    cache: bool


args_to_cache = [
    "string",
    100,
    100.1,
    None,
    True,
    False,
    {"cache": True},
    SchemaForTest(cache=True),
    [SchemaForTest(cache=True), SchemaForTest(cache=True)],
    ["string", "other_string"],
    set([1, 2, 3]),
    (1, 2, 3),
]


class TestCacheBuilder:
    @pytest.mark.parametrize("arg", args_to_cache)
    def test_cache_key_builder_same_args(self, arg):
        def task(payload):
            return payload

        prefix = uuid4().hex
        first = KeyBuilder(prefix, task, arg)
        second = KeyBuilder(prefix, task, deepcopy(arg))
        assert first.key == second.key

    def test_cache_key_builder_same_kwargs(self):
        filters = {"id": 1}

        def task(filters: dict = {}):
            return filters

        prefix = uuid4().hex
        first = KeyBuilder(prefix, task, filters=filters)
        second = KeyBuilder(prefix, task, filters=filters)
        assert first.key == second.key

    def test_cache_key_builder_same_args_kwargs(self):
        filters = {"id": 1}

        def task(filters: dict = {}):
            return filters

        prefix = uuid4().hex
        args = KeyBuilder(prefix, task, filters)
        kwargs = KeyBuilder(prefix, task, filters=filters)
        assert args.key == kwargs.key

    def test_cache_key_builder_diff_args(self):
        filters = {"id": 1}

        def task(filters: dict = {}):
            return filters

        prefix = uuid4().hex
        args = KeyBuilder(prefix, task, filters)
        kwargs = KeyBuilder(prefix, task, {"id": 2})
        assert args.key != kwargs.key

    def test_cache_key_builder_diff_kwargs(self):
        filters = {"id": 1}

        def task(filters: dict = {}):
            return filters

        prefix = uuid4().hex
        args = KeyBuilder(prefix, task, filters=filters)
        kwargs = KeyBuilder(prefix, task, filters={"id": 2})
        assert args.key != kwargs.key

    def test_cache_key_builder_diff_args_and_kwargs(self):
        filters = {"id": 1}

        def task(filters: dict = {}):
            return filters

        prefix = uuid4().hex
        args = KeyBuilder(prefix, task, filters)
        kwargs = KeyBuilder(prefix, task, filters={"id": 2})
        assert args.key != kwargs.key

    def test_cache_key_builder_diff_order_kwargs(self):
        def task(a, b):
            return a, b

        prefix = uuid4().hex
        first = KeyBuilder(prefix, task, a=1, b=2)
        second = KeyBuilder(prefix, task, b=2, a=1)
        assert first.key == second.key
