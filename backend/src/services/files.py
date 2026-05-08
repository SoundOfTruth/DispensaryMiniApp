import uuid
from typing import Annotated

import aiofiles
from fastapi import Depends, UploadFile
from pydantic import HttpUrl

from services.exceptions import InvalidFileExtensionError
from src.config import settings
from src.schemas.files import UploadResponse

allowed_types = "|".join(["jpeg", "png", "webp", "avif", "apng"])


class FileService:
    async def create(self, base_url: str, file: UploadFile):
        if not file.content_type:
            raise InvalidFileExtensionError
        file_type, ext = file.content_type.split("/")
        if file_type != "image" or ext not in allowed_types:
            raise InvalidFileExtensionError
        content = await file.read()
        filepath = f"{settings.MEDIA_DIR}/{uuid.uuid4()}.{ext}"
        async with aiofiles.open(filepath, "wb") as f:
            await f.write(content)
        return UploadResponse(url=HttpUrl(f"{base_url}{filepath}"))


FileServiceDep = Annotated[FileService, Depends()]
