from typing import Annotated

from fastapi import Depends

from src.cache.manager import CacheManager
from src.database.core import AsyncScopedSessionDep
from src.repositories.equipment_types import EquipmentTypeRepository
from src.schemas.equipments import (
    CreateEquipmentTypeSchema,
    EquipmentTypeSchema,
    SimpleEquipmentTypeSchema,
    UpdateEquipmentTypeSchema,
)
from src.services.exceptions import NotFoundError

cache = CacheManager("equipment-type")


class EquipmentTypeService:
    def __init__(self, session: AsyncScopedSessionDep) -> None:
        self.equipment_rep = EquipmentTypeRepository(session=session)

    @cache.expire
    async def create(
        self, schema: CreateEquipmentTypeSchema
    ) -> SimpleEquipmentTypeSchema:
        equipment = await self.equipment_rep.create(schema.model_dump())
        return SimpleEquipmentTypeSchema.model_validate(equipment)

    @cache.expire
    async def update(
        self, id: int, schema: UpdateEquipmentTypeSchema
    ) -> SimpleEquipmentTypeSchema:
        equipment_type = await self.equipment_rep.update(id, schema.model_dump())
        if not equipment_type:
            raise NotFoundError
        return SimpleEquipmentTypeSchema.model_validate(equipment_type)

    @cache.use
    async def get_all_with_relations(self) -> list[EquipmentTypeSchema]:
        equipment_types = await self.equipment_rep.get_all_with_relations()
        return [
            EquipmentTypeSchema.model_validate(equipment_type)
            for equipment_type in equipment_types
        ]

    @cache.use
    async def get_all(self, search: str | None) -> list[SimpleEquipmentTypeSchema]:
        equipment_types = await self.equipment_rep.get_all(search)
        return [
            SimpleEquipmentTypeSchema.model_validate(equipment_type)
            for equipment_type in equipment_types
        ]

    @cache.use
    async def get(self, id: int) -> SimpleEquipmentTypeSchema:
        equipment_type = await self.equipment_rep.get(id)
        if not equipment_type:
            raise NotFoundError
        return SimpleEquipmentTypeSchema.model_validate(equipment_type)

    @cache.expire
    async def delete(self, id: int):
        return await self.equipment_rep.delete(id)


EquipmentTypeServiceDep = Annotated[EquipmentTypeService, Depends()]
