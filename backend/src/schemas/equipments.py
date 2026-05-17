from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class CreateEquipmentTypeSchema(BaseModel):
    name: str = Field(max_length=255)

    model_config = ConfigDict(str_min_length=1)


class UpdateEquipmentTypeSchema(BaseModel):
    name: str = Field(max_length=255)

    model_config = ConfigDict(str_min_length=1)


class CreateEquipmentSchema(BaseModel):
    name: str = Field(max_length=255)
    type_id: int
    image: HttpUrl

    model_config = ConfigDict(str_min_length=1)


class UpdateEquipmentSchema(BaseModel):
    name: str = Field(default="", max_length=255)
    type_id: int = Field(default=0, gt=0)
    image: HttpUrl = HttpUrl("http://localhost/err.png")

    model_config = ConfigDict(str_min_length=1)


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
