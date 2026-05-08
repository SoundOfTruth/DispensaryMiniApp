from typing import Annotated

from fastapi import Depends

from src.database.core import AsyncScopedSessionDep
from src.repositories.equipments import EquipmentRepository
from src.schemas.equipments import (
    CreateEquipmentSchema,
    EquipmentSchema,
    UpdateEquipmentSchema,
)
from src.services.exceptions import EmptyPatchError, NotFoundError


class EquipmentsService:
    def __init__(self, session: AsyncScopedSessionDep) -> None:
        self.equipment_rep = EquipmentRepository(session=session)

    async def create(self, schema: CreateEquipmentSchema):
        equipment = await self.equipment_rep.create(schema.model_dump())
        return EquipmentSchema.model_validate(equipment)

    async def update(self, id: int, schema: UpdateEquipmentSchema):
        payload = schema.model_dump(exclude_unset=True)
        if not payload:
            raise EmptyPatchError
        equipment = await self.equipment_rep.update(id, payload)
        if not equipment:
            raise NotFoundError
        return EquipmentSchema.model_validate(equipment)

    async def get_all(self):
        equipments = await self.equipment_rep.get_all_with_relations()
        return [EquipmentSchema.model_validate(equipment) for equipment in equipments]

    async def get(self, id: int):
        equipment = await self.equipment_rep.get_with_relations(id)
        if not equipment:
            raise NotFoundError
        return EquipmentSchema.model_validate(equipment)

    async def delete(self, id: int):
        return await self.equipment_rep.delete(id)

    async def bulk_delete(self, ids: list[int]):
        return await self.equipment_rep.bulk_delete(ids)


EquipmentServiceDep = Annotated[EquipmentsService, Depends()]
