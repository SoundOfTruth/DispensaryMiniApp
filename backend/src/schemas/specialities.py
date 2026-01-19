from pydantic import ConfigDict

from src.schemas.base import BaseSchema


class CreateSpecialitySchema(BaseSchema):
    name: str


class SpecialitySchema(CreateSpecialitySchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
