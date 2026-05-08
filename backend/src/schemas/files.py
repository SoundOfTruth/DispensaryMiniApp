from pydantic import BaseModel, HttpUrl


class UploadResponse(BaseModel):
    url: HttpUrl
