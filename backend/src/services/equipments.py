from typing import Annotated

from fastapi import Depends

from src.database.core import AsyncScopedSessionDep
from src.repositories.equipments import EquipmentRepository
from src.schemas.equipments import (
    CreateEquipmentSchema,
    EquipmentSchema,
    SimpleEquipmentSchema,
    UpdateEquipmentSchema,
)
from src.services.exceptions import EmptyPatchError, NotFoundError


class EquipmentsService:
    def __init__(self, session: AsyncScopedSessionDep) -> None:
        self.equipment_rep = EquipmentRepository(session=session)

    async def create(self, schema: CreateEquipmentSchema, base_url: str):
        equipment = await self.equipment_rep.create(schema.model_dump(mode="json"))
        if base_url not in str(schema.image):
            raise
        return SimpleEquipmentSchema.model_validate(equipment)

    async def update(self, id: int, schema: UpdateEquipmentSchema, base_url: str):
        payload = schema.model_dump(mode="json", exclude_unset=True)
        if not payload:
            raise EmptyPatchError
        image = payload.get("image")
        if image and base_url not in image:
            raise
        equipment = await self.equipment_rep.update(id, payload)
        if not equipment:
            raise NotFoundError
        return SimpleEquipmentSchema.model_validate(equipment)

    async def get_all(self, search: str | None):
        equipments = await self.equipment_rep.get_all_with_relations(search)
        return [EquipmentSchema.model_validate(equipment) for equipment in equipments]

    async def get(self, id: int):
        equipment = await self.equipment_rep.get_with_relations(id)
        if not equipment:
            raise NotFoundError
        return SimpleEquipmentSchema.model_validate(equipment)

    async def delete(self, id: int):
        return await self.equipment_rep.delete(id)

    async def bulk_delete(self, ids: list[int]):
        return await self.equipment_rep.bulk_delete(ids)


EquipmentServiceDep = Annotated[EquipmentsService, Depends()]
