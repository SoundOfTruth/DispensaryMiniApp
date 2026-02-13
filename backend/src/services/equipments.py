from typing import Annotated

from fastapi import Depends

from src.database.core import AsyncScopedSessionDep
from src.repositories.equipments import EquipmentRepository
from src.schemas.equipments import (
    CreateEquipmentSchema,
    CreateEquipmentTypeSchema,
    EquimentSchema,
    EquipmentByTypeSchema,
)


class EquipmentsService:
    def __init__(self, session: AsyncScopedSessionDep) -> None:
        self.equipment_repo = EquipmentRepository(session=session)

    async def get_all_grouped(self):
        equipments = await self.equipment_repo.get_all_grouped()
        return [
            EquipmentByTypeSchema.model_validate(equipment) for equipment in equipments
        ]

    async def get(self, id):
        equipment = await self.equipment_repo.get_with_relations(id)
        return EquimentSchema.model_validate(equipment)

    async def get_all(self):
        equipments = await self.equipment_repo.get_all_with_relations()
        return [EquimentSchema.model_validate(equipment) for equipment in equipments]

    async def create(self, schema: CreateEquipmentSchema):
        return await self.equipment_repo.create(schema.model_dump())

    async def create_type(self, schema: CreateEquipmentTypeSchema):
        return await self.equipment_repo.create_type(schema.model_dump())

    async def get_types(self):
        return await self.equipment_repo.get_types()

    async def get_type(self, id: int):
        return await self.equipment_repo.get_type(id)


EquipmentServiceDep = Annotated[EquipmentsService, Depends(EquipmentsService)]
