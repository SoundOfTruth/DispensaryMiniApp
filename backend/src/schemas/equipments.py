from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.base import BaseSchema, FileField


class CreateEquipmentTypeSchema(BaseSchema):
    name: str = Field(max_length=255)


class UpdateEquipmentTypeSchema(BaseSchema):
    name: str = Field(max_length=255)


class CreateEquipmentSchema(BaseSchema):
    name: str = Field(max_length=255)
    type_id: int
    image: FileField


class UpdateEquipmentSchema(BaseSchema):
    name: str = Field(default="", max_length=255)
    type_id: int = Field(default=0, gt=0)
    image: FileField = Field(default_factory=lambda: f"/media/{uuid4()}")


class SimpleEquipmentSchema(CreateEquipmentSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class EquipmentSchema(CreateEquipmentSchema):
    id: int
    type_id: int = Field(exclude=True)
    type: "SimpleEquipmentTypeSchema"

    model_config = ConfigDict(from_attributes=True)


class EquipmentItemSchema(BaseModel):
    id: int
    name: str
    image: str

    model_config = ConfigDict(from_attributes=True)


class SimpleEquipmentTypeSchema(CreateEquipmentTypeSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class EquipmentTypeSchema(SimpleEquipmentTypeSchema):
    equipments: list[EquipmentItemSchema]

    model_config = ConfigDict(from_attributes=True)
