from asgiref.sync import async_to_sync
from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.config import settings
from src.services.files import FileService


async def _delete_unlinked_files():
    engine = create_async_engine(settings.DATABASE.URL_ASYNCPG)
    try:
        async with AsyncSession(bind=engine) as session:
            await FileService().delete_unlinked_files(session)
    finally:
        await engine.dispose()


@shared_task
def delete_unlinked_files():
    async_to_sync(_delete_unlinked_files)()
