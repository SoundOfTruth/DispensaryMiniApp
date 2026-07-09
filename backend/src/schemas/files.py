from pydantic import BaseModel

from src.schemas.base import FileField


class UploadResponse(BaseModel):
    url: FileField
