from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.models.equipments import Equipment, EquipmentType
from src.repositories.base import DefaultRepository


class EquipmentRepository(DefaultRepository[Equipment]):
    model = Equipment

    async def get_all_grouped_by_type(self):
        statement = (
            select(EquipmentType)
            .options(selectinload(EquipmentType.equipments))
            .where(EquipmentType.equipments.any())
        )
        res = await self.session.execute(statement)
        return res.scalars().all()

    async def get_with_relations(self, id: int) -> Equipment | None:
        statement = (
            select(self.model)
            .where(Equipment.id == id)
            .options(joinedload(self.model.type))
        )
        res = await self.session.execute(statement)
        return res.scalar_one_or_none()

    async def get_all_with_relations(self) -> Sequence[Equipment]:
        statement = select(self.model).options(joinedload(self.model.type))
        res = await self.session.execute(statement)
        return res.scalars().all()

    async def create(self, data: dict) -> Equipment:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def create_type(self, data: dict) -> EquipmentType:
        instance = EquipmentType(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get_types(self):
        statement = select(EquipmentType)
        res = await self.session.execute(statement)
        return res.scalars().all()

    async def get_type(self, id: int):
        statement = select(EquipmentType).where(EquipmentType.id == id)
        res = await self.session.execute(statement)
        return res.scalars().all()
