from typing import Annotated

from fastapi import Depends

from src.database.core import AsyncScopedSessionDep
from src.repositories.equipment_types import EquipmentTypeRepository
from src.schemas.equipments import (
    CreateEquipmentTypeSchema,
    EquipmentTypeSchema,
    SimpleEquipmentTypeSchema,
    UpdateEquipmentTypeSchema,
)
from src.services.exceptions import NotFoundError


class EquipmentTypeService:
    def __init__(self, session: AsyncScopedSessionDep) -> None:
        self.equipment_rep = EquipmentTypeRepository(session=session)

    async def create(self, schema: CreateEquipmentTypeSchema):
        equipment = await self.equipment_rep.create(schema.model_dump())
        return SimpleEquipmentTypeSchema.model_validate(equipment)

    async def update(self, id: int, schema: UpdateEquipmentTypeSchema):
        equipment_type = await self.equipment_rep.update(id, schema.model_dump())
        if not equipment_type:
            raise NotFoundError
        return SimpleEquipmentTypeSchema.model_validate(equipment_type)

    async def get_all_with_relations(self):
        equipment_types = await self.equipment_rep.get_all_with_relations()
        return [
            EquipmentTypeSchema.model_validate(equipment_type)
            for equipment_type in equipment_types
        ]

    async def get_all(self):
        equipment_types = await self.equipment_rep.get_all()
        return [
            SimpleEquipmentTypeSchema.model_validate(equipment_type)
            for equipment_type in equipment_types
        ]

    async def get(self, id: int):
        equipment_type = await self.equipment_rep.get(id)
        if not equipment_type:
            raise NotFoundError
        return SimpleEquipmentTypeSchema.model_validate(equipment_type)

    async def delete(self, id: int):
        return await self.equipment_rep.delete(id)

    async def bulk_delete(self, ids: list[int]):
        return await self.equipment_rep.bulk_delete(ids)


EquipmentTypeServiceDep = Annotated[EquipmentTypeService, Depends()]
