from asyncio import current_task
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


class Base(DeclarativeBase, AsyncAttrs):
    pass


async_engine = create_async_engine(url=settings.DATABASE_URL_ASYNCPG, echo=False)

AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False)

AsyncSessionScoped = async_scoped_session(
    session_factory=AsyncSessionLocal, scopefunc=current_task
)


async def async_session_scoped_gen():
    async with AsyncSessionScoped() as session:
        yield session


AsyncScopedSessionDep = Annotated[AsyncSession, Depends(async_session_scoped_gen)]
