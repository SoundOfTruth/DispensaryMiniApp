from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from src.models.equipments import Equipment
from src.repositories.base import DefaultRepository
from src.repositories.exceptions import (
    EquipmentNameAlreadyExistsError,
    EquipmentTypeNotExistsError,
)


class EquipmentRepository(DefaultRepository[Equipment]):
    model = Equipment

    async def handle_error(self, err: IntegrityError):
        await self.session.rollback()
        orig_err = str(err.orig)
        if "equipments_name_key" in orig_err:
            raise EquipmentNameAlreadyExistsError
        if "equipments_type_id_fkey" in orig_err:
            raise EquipmentTypeNotExistsError
        raise err

    async def count(self) -> int:
        return await super()._count()

    async def create(self, data: dict) -> Equipment:
        instance = self.model(**data)
        self.session.add(instance)
        try:
            await self.session.commit()
        except IntegrityError as ex:
            await self.handle_error(ex)
        else:
            return instance

    async def update(self, id: int, data: dict) -> Equipment | None:
        statement = (
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .returning(self.model)
        )
        try:
            res = await self.session.execute(statement)
            await self.session.commit()
        except IntegrityError as ex:
            await self.handle_error(ex)
        else:
            return res.scalar_one_or_none()

    async def get_all_with_relations(self) -> Sequence[Equipment]:
        statement = select(self.model).options(joinedload(self.model.type))
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
