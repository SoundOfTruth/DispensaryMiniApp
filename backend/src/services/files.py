import logging
import uuid
from pathlib import Path
from typing import Annotated

import aiofiles
from fastapi import Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.repositories.doctors import DoctorRepository
from src.repositories.equipments import EquipmentRepository
from src.schemas.files import UploadResponse
from src.services.exceptions import InvalidFileExtensionError

log = logging.getLogger("error_handler")
allowed_types = "|".join(["jpeg", "png", "webp", "avif", "apng"])


class FileService:
    async def create(self, file: UploadFile) -> UploadResponse:
        if not file.content_type:
            raise InvalidFileExtensionError
        file_type, ext = file.content_type.split("/")
        if file_type != "image" or ext not in allowed_types:
            raise InvalidFileExtensionError
        content = await file.read()
        filename = f"{uuid.uuid4()}.{ext}"
        filepath = f"{settings.MEDIA_DIR}/{filename}"
        async with aiofiles.open(filepath, "wb") as f:
            await f.write(content)
        return UploadResponse(url=f"/{settings.MEDIA_URL}/{filename}")

    async def get_linked_files(self, session: AsyncSession) -> set[str]:
        media_links: set[str] = set()
        equipments = await EquipmentRepository(session).get_all()
        doctors = await DoctorRepository(session).get_all()
        for equipment in equipments:
            media_links.add(Path(equipment.image).name)
        for doctor in doctors:
            if doctor.photo:
                media_links.add(Path(doctor.photo).name)
        return media_links

    async def delete_unlinked_files(self, session: AsyncSession):
        media_path = Path(settings.MEDIA_DIR)
        all_files: set[str] = set(
            file.name for file in media_path.iterdir() if file.is_file()
        )
        linked_files: set[str] = await self.get_linked_files(session)
        unlinked_files = all_files - linked_files

        def delete_files():
            for file in unlinked_files:
                try:
                    (media_path / file).unlink()
                except FileNotFoundError as ex:
                    log.exception("Task File Not Found", exc_info=ex)

        delete_files()


FileServiceDep = Annotated[FileService, Depends()]
