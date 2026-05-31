from contextlib import asynccontextmanager

import pytest_asyncio
from httpx import ASGITransport, AsyncClient, Auth

from src.database.core import async_session_scoped_gen
from src.main import app
from src.schemas.users import UserSchema
from src.utils.auth import create_access_token, create_refresh_token


class TokenAuth(Auth):
    def __init__(self, token, schema="Bearer"):
        self.token = f"{schema} {token}"

    def auth_flow(self, request):
        request.headers["Authorization"] = self.token
        yield request


@pytest_asyncio.fixture
async def user_access_token(user):
    schema = UserSchema.model_validate(user)
    return create_access_token(schema)


@pytest_asyncio.fixture
async def admin_access_token(admin):
    schema = UserSchema.model_validate(admin)
    return create_access_token(schema)


@pytest_asyncio.fixture
async def superuser_access_token(superuser):
    schema = UserSchema.model_validate(superuser)
    return create_access_token(schema)


@pytest_asyncio.fixture
async def create_client(session):
    @asynccontextmanager
    async def wrapper(token: str | None = None):
        async def override_db():
            yield session

        app.dependency_overrides[async_session_scoped_gen] = override_db

        async with AsyncClient(
            auth=TokenAuth(token),
            base_url="http://test",
            transport=ASGITransport(app=app),
        ) as client:
            yield client

        app.dependency_overrides.clear()

    return wrapper


@pytest_asyncio.fixture
async def client(create_client):
    async with create_client(user_access_token) as client:
        yield client


@pytest_asyncio.fixture
async def user_client(create_client, user_access_token):
    async with create_client(user_access_token) as client:
        yield client


@pytest_asyncio.fixture
async def admin_client(create_client, admin_access_token):
    async with create_client(admin_access_token) as client:
        yield client


@pytest_asyncio.fixture
async def superuser_client(create_client, superuser_access_token):
    async with create_client(superuser_access_token) as client:
        yield client


@pytest_asyncio.fixture
async def user_refresh_token(user):
    schema = UserSchema.model_validate(user)
    return create_refresh_token(schema)


@pytest_asyncio.fixture
async def admin_refresh_token(admin):
    schema = UserSchema.model_validate(admin)
    return create_refresh_token(schema)


@pytest_asyncio.fixture
async def superuser_refresh_token(superuser):
    schema = UserSchema.model_validate(superuser)
    return create_refresh_token(schema)
