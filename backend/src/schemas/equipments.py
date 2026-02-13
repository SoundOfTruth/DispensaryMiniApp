from pydantic import BaseModel, ConfigDict, field_serializer


class CreateEquipmentSchema(BaseModel):
    name: str
    type_id: int
    image: str | None


class EquimentSchema(BaseModel):
    name: str
    image: str | None

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


class EquipmentByTypeSchema(EquipmentTypeSchema):
    equipments: list[EquimentSchema]
