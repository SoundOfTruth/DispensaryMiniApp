from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from src.models.doctors import Speciality
from src.repositories.base import DefaultRepository
from src.repositories.exceptions import (
    SpecialityIsUsingError,
    SpecialityNameAlreadyExistsError,
)


class SpecialityRepository(DefaultRepository[Speciality]):
    model = Speciality

    async def handle_error(self, err: IntegrityError):
        await self.session.rollback()
        orig_err = str(err.orig)
        if "specialities_name_key" in orig_err:
            raise SpecialityNameAlreadyExistsError
        if "doctors_speciality_id_fkey" in orig_err:
            raise SpecialityIsUsingError
        raise err

    async def count(self) -> int:
        return await super()._count()

    async def create(self, data: dict) -> Speciality:
        instance = self.model(**data)
        self.session.add(instance)
        try:
            await self.session.commit()
        except IntegrityError as ex:
            await self.handle_error(ex)
        else:
            return instance

    async def update(self, id: int, data: dict) -> Speciality | None:
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
