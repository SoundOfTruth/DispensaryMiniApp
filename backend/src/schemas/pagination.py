from pydantic import BaseModel, Field

from src.config import settings


class PaginationParams(BaseModel):
    limit: int = Field(default=settings.PAGINATION_SIZE, gt=0, le=100)
    offset: int = Field(default=0, gt=-1)
