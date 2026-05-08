from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from src.config import settings

test_async_engine = create_async_engine(
    url=settings.DATABASE.URL_TEST_ASYNCPG, echo=False
)

TestAsyncSessionLocal = async_sessionmaker(
    bind=test_async_engine, expire_on_commit=False
)

TestAsyncSessionScoped = async_scoped_session(
    session_factory=TestAsyncSessionLocal, scopefunc=current_task
)


async def test_async_session_scoped_generator():
    async with TestAsyncSessionScoped() as session:
        yield session
