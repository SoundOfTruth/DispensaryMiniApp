from pydantic import ConfigDict

from src.schemas.base import BaseSchema


class CreateDepartmentShema(BaseSchema):
    name: str


class DepartmentSchema(CreateDepartmentShema):
    id: int

    model_config = ConfigDict(from_attributes=True)
