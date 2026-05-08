from pydantic import ConfigDict, Field

from src.schemas.base import BaseSchema


class CreateSpecialitySchema(BaseSchema):
    name: str = Field(max_length=255)


class UpdateSpecialitySchema(BaseSchema):
    name: str = Field(max_length=255)


class SpecialitySchema(CreateSpecialitySchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
