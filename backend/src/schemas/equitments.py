from src.schemas.base import BaseSchema


class CreateEquipmentSchema(BaseSchema):
    name: str
    image: str | None


class EquipmentsSchema(CreateEquipmentSchema):
    id: int
