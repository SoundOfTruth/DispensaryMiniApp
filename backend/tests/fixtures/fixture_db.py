import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.config import settings


@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine(
        url=settings.DATABASE.URL_TEST_ASYNCPG,
        echo=False,
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine):
    connection = await engine.connect()
    transaction = await connection.begin()
    session = AsyncSession(
        bind=connection,
        expire_on_commit=False,
    )

    yield session
    await transaction.rollback()
    await session.close()
    await connection.close()
