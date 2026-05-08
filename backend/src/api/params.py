from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, Field, PositiveInt

from src.config import settings

QueryIds = Annotated[
    list[PositiveInt],
    Query(
        min_length=1,
        max_length=100,
    ),
]


class PaginationParams(BaseModel):
    limit: int = Field(default=settings.PAGINATION_SIZE, gt=0, le=100)
    offset: int = Field(default=0, gt=-1)
