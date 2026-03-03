from pydantic import BaseModel, PositiveInt


class PaginationParams(BaseModel):
    page: PositiveInt = 1
