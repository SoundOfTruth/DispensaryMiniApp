from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.services.files import FileService


class TestTasks:
    async def test_cleanup_unlinked_files(
        self, session: AsyncSession, unlinked_files: list[str]
    ):
        service = FileService()
        assert len(unlinked_files) > 1
        await service.delete_unlinked_files(session)
        for file in unlinked_files:
            file_path = Path(settings.MEDIA_DIR) / Path(file).name
            assert not file_path.exists()

    async def test_cleanup_linked_files(
        self, session: AsyncSession, linked_files: list[str]
    ):
        service = FileService()
        assert len(linked_files) > 1
        await service.delete_unlinked_files(session)
        for file in linked_files:
            file_path = Path(settings.MEDIA_DIR) / Path(file).name
            assert file_path.exists()

    async def test_cleanup_linked_any_files(
        self,
        session: AsyncSession,
        any_files: list[str],
        linked_files: list[str],
        unlinked_files: list[str],
    ):
        service = FileService()
        assert len(any_files) > 1
        await service.delete_unlinked_files(session)
        for file in unlinked_files:
            file_path = Path(settings.MEDIA_DIR) / Path(file).name
            assert not file_path.exists()
        for file in linked_files:
            file_path = Path(settings.MEDIA_DIR) / Path(file).name
            assert file_path.exists()
