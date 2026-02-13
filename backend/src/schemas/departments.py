from pydantic import ConfigDict

from src.schemas.base import BaseSchema


class CreateDepartmentSchema(BaseSchema):
    name: str


class DepartmentSchema(CreateDepartmentSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
