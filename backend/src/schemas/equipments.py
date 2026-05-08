from pydantic import BaseModel, ConfigDict, Field


class CreateEquipmentTypeSchema(BaseModel):
    name: str = Field(max_length=255)

    model_config = ConfigDict(str_min_length=1)


class UpdateEquipmentTypeSchema(BaseModel):
    name: str = Field(max_length=255)

    model_config = ConfigDict(str_min_length=1)


class CreateEquipmentSchema(BaseModel):
    name: str = Field(max_length=255)
    type_id: int
    image: str | None = None

    model_config = ConfigDict(str_min_length=1)


class UpdateEquipmentSchema(BaseModel):
    name: str = Field(default="", max_length=255)
    type_id: int = Field(default=0, gt=0)
    image: str | None = None

    model_config = ConfigDict(str_min_length=1)


class EquipmentSchema(CreateEquipmentSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class EquipmentItemSchema(BaseModel):
    id: int
    name: str
    image: str | None

    model_config = ConfigDict(from_attributes=True)


class SimpleEquipmentTypeSchema(CreateEquipmentTypeSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class EquipmentTypeSchema(SimpleEquipmentTypeSchema):
    equipments: list[EquipmentItemSchema]

    model_config = ConfigDict(from_attributes=True)
