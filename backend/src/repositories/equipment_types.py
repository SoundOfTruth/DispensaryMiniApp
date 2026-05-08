from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from src.models.equipments import EquipmentType
from src.repositories.base import DefaultRepository
from src.repositories.exceptions import (
    EquipmentTypeIsUsingError,
    EquipmentTypeNameAlreadyExistsError,
)


class EquipmentTypeRepository(DefaultRepository):
    model = EquipmentType

    async def handle_error(self, err: IntegrityError):
        await self.session.rollback()
        orig_err = str(err.orig)
        if "equipment_types_name_key" in orig_err:
            raise EquipmentTypeNameAlreadyExistsError
        if "equipments_type_id_fkey" in orig_err:
            raise EquipmentTypeIsUsingError
        raise err

    async def create(self, data: dict) -> EquipmentType:
        instance = EquipmentType(**data)
        self.session.add(instance)
        try:
            await self.session.commit()
        except IntegrityError as ex:
            await self.handle_error(ex)
        else:
            return instance

    async def update(self, id: int, data: dict) -> EquipmentType | None:
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

    async def get_all_with_relations(self) -> Sequence[EquipmentType]:
        statement = (
            select(self.model)
            .options(selectinload(self.model.equipments))
            .where(self.model.equipments.any())
        )
        res = await self.session.execute(statement)
        return res.scalars().all()
