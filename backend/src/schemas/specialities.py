from pydantic import ConfigDict

from src.schemas.base import BaseSchema


class CreateSpecialityShema(BaseSchema):
    name: str


class SpecialitySchema(CreateSpecialityShema):
    id: int

    model_config = ConfigDict(from_attributes=True)
