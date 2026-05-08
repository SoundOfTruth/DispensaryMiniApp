from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from repositories.exceptions import (
    DepartmentIsUsingError,
    DepartmentNameAlreadyExistsError,
)
from src.models.doctors import Department
from src.repositories.base import DefaultRepository


class DepartmentRepository(DefaultRepository[Department]):
    model = Department

    async def handle_error(self, err: IntegrityError):
        await self.session.rollback()
        orig_err = str(err.orig)
        if "department_name_key" in orig_err:
            raise DepartmentNameAlreadyExistsError
        if "doctors_department_id_fkey" in orig_err:
            raise DepartmentIsUsingError
        raise err

    async def count(self) -> int:
        return await super()._count()

    async def create(self, data: dict) -> Department:
        instance = Department(**data)
        self.session.add(instance)
        try:
            await self.session.commit()
        except IntegrityError as ex:
            await self.handle_error(ex)
        else:
            return instance

    async def update(self, id: int, data: dict) -> Department | None:
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
