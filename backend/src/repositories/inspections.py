from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from src.models import Doctor, DoctorInspection, Inspection
from src.repositories.base import DeleteOnlyRepository
from src.repositories.exceptions import (
    InspectionDoctorNotExistsError,
    InspectionTitleAlreadyExistsError,
    InspectionWasDeletedError,
)


class InspectionRepository(DeleteOnlyRepository[Inspection]):
    model = Inspection

    async def handle_error(self, err: IntegrityError):
        await self.session.rollback()
        orig_err = str(err.orig)
        if "inspections_title_key" in orig_err:
            raise InspectionTitleAlreadyExistsError
        elif "doctor_inspections_doctor_id_fkey" in orig_err:
            raise InspectionDoctorNotExistsError
        raise err

    def get_expressions(self, search: str | None) -> list:
        expressions = []
        if search:
            expressions.append(self.model.title.icontains(search))
        return expressions

    async def count(self, search: str | None = None) -> int:
        expressions = self.get_expressions(search)
        return await self._count(expressions=expressions)

    async def get_with_relations(self, id: int) -> Inspection | None:
        options = [
            selectinload(self.model.doctors).joinedload(Doctor.speciality),
            selectinload(self.model.doctors).joinedload(Doctor.department),
        ]
        statement = select(self.model).where(self.model.id == id).options(*options)
        res = await self.session.execute(statement)
        return res.scalar_one_or_none()

    async def get_all(
        self, search: str | None, limit: int | None = None, offset: int | None = None
    ) -> Sequence[Inspection]:
        expressions = self.get_expressions(search)
        statement = select(self.model).where(*expressions).limit(limit).offset(offset)
        res = await self.session.execute(statement)
        return res.scalars().all()

    async def create(self, data: dict) -> Inspection:
        doctors = data.pop("doctors", [])
        instance = self.model(**data)
        instance.inspection_doctors = [DoctorInspection(**doctor) for doctor in doctors]
        self.session.add(instance)
        try:
            await self.session.commit()
        except IntegrityError as ex:
            await self.handle_error(ex)
        else:
            inspection = await self.get_with_relations(instance.id)
            if not inspection:
                raise InspectionWasDeletedError
            return inspection

    async def update(self, id: int, data: dict) -> Inspection | None:
        doctors: list[dict] | None = data.pop("doctors", None)
        instance = await self.get_with_relations(id)
        if not instance:
            return None
        if doctors is not None:
            await instance.awaitable_attrs.inspection_doctors
            instance.inspection_doctors = [
                DoctorInspection(**doctor) for doctor in doctors
            ]
        for attr in data:
            setattr(instance, attr, data[attr])
        try:
            await self.session.commit()
        except IntegrityError as ex:
            await self.handle_error(ex)
        else:
            self.session.expire(instance)
            inspection = await self.get_with_relations(id)
            if not inspection:
                raise InspectionWasDeletedError
            return inspection
