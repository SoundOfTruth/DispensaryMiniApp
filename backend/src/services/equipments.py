from typing import Annotated

from fastapi import Depends

from src.cache.manager import CacheManager
from src.database.core import AsyncScopedSessionDep
from src.repositories.equipments import EquipmentRepository
from src.schemas.equipments import (
    CreateEquipmentSchema,
    EquipmentSchema,
    SimpleEquipmentSchema,
    UpdateEquipmentSchema,
)
from src.services.exceptions import EmptyPatchError, NotFoundError

cache = CacheManager("equipment")


class EquipmentsService:
    def __init__(self, session: AsyncScopedSessionDep) -> None:
        self.equipment_rep = EquipmentRepository(session=session)

    @cache.expire
    async def create(self, schema: CreateEquipmentSchema) -> SimpleEquipmentSchema:
        equipment = await self.equipment_rep.create(schema.model_dump(mode="json"))
        return SimpleEquipmentSchema.model_validate(equipment)

    @cache.expire
    async def update(
        self, id: int, schema: UpdateEquipmentSchema
    ) -> SimpleEquipmentSchema:
        payload = schema.model_dump(mode="json", exclude_unset=True)
        if not payload:
            raise EmptyPatchError
        equipment = await self.equipment_rep.update(id, payload)
        if not equipment:
            raise NotFoundError
        return SimpleEquipmentSchema.model_validate(equipment)

    @cache.use
    async def get_all(self, search: str | None) -> list[EquipmentSchema]:
        equipments = await self.equipment_rep.get_all_with_relations(search)
        return [EquipmentSchema.model_validate(equipment) for equipment in equipments]

    @cache.use
    async def get(self, id: int) -> SimpleEquipmentSchema:
        equipment = await self.equipment_rep.get_with_relations(id)
        if not equipment:
            raise NotFoundError
        return SimpleEquipmentSchema.model_validate(equipment)

    @cache.expire
    async def delete(self, id: int):
        return await self.equipment_rep.delete(id)


EquipmentServiceDep = Annotated[EquipmentsService, Depends()]
