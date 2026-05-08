from pydantic import ConfigDict, Field

from src.schemas.base import BaseSchema


class CreateDepartmentSchema(BaseSchema):
    name: str = Field(max_length=255)


class UpdateDepartmentSchema(BaseSchema):
    name: str = Field(max_length=255)


class DepartmentSchema(CreateDepartmentSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
