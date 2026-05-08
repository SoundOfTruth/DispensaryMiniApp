import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app
from tests.core import TestAsyncSessionLocal


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def session(anyio_backend):
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(
        base_url="http://test",
        transport=ASGITransport(app=app),
    ) as client:
        yield client
