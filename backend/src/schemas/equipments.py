from pydantic import BaseModel, ConfigDict, Field, field_serializer


class CreateEquipmentSchema(BaseModel):
    name: str
    type_id: int
    image: str | None


class SimpleEquimentSchema(BaseModel):
    id: int
    name: str
    image: str | None

    model_config = ConfigDict(from_attributes=True)


class EquimentSchema(SimpleEquimentSchema):
    type: "EquipmentTypeSchema"

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("type")
    def serialize_type(self, obj: "EquipmentTypeSchema"):
        return obj.name


class CreateEquipmentTypeSchema(BaseModel):
    name: str


class EquipmentTypeSchema(CreateEquipmentTypeSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class EquipmentByTypeSchema(BaseModel):
    name: str = Field(serialization_alias="type")

    equipments: list[SimpleEquimentSchema]

    model_config = ConfigDict(from_attributes=True, serialize_by_alias=True)
