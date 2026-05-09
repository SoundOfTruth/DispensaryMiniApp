from typing import Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, selectinload, with_expression

from src.models import Doctor, DoctorInspection, Education, ExtraEducation
from src.repositories.base import DeleteOnlyRepository
from src.repositories.exceptions import (
    DoctorDepartmentNotExistsError,
    DoctorInspectionNotExistsError,
    DoctorInvalidExpirienctStartError,
    DoctorSpecialityNotExistsError,
    DoctorWasDeletedError,
)


class DoctorRepository(DeleteOnlyRepository[Doctor]):
    model = Doctor

    async def handle_error(self, err: IntegrityError):
        await self.session.rollback()
        origx_err = str(err.orig)
        if "check_experience_start" in origx_err:
            raise DoctorInvalidExpirienctStartError
        if "doctors_speciality_id_fkey" in origx_err:
            raise DoctorSpecialityNotExistsError
        if "doctors_department_id_fkey" in origx_err:
            raise DoctorDepartmentNotExistsError
        if "doctor_inspections_inspection_id_fkey" in origx_err:
            raise DoctorInspectionNotExistsError
        raise err

    def get_search_expressions(self, search: str | None):
        expressions = []
        if search:
            expressions.append(
                or_(
                    self.model.lastname.icontains(search),
                    self.model.firstname.icontains(search),
                    self.model.middlename.icontains(search),
                )
            )
        return expressions

    async def count(
        self, filters: dict[str, int] = {}, search: str | None = None
    ) -> int:
        expressions = self.get_search_expressions(search)
        return await self._count(filters, expressions)

    async def get_all(
        self,
        search: str | None = None,
        filters: dict[str, int] = {},
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[Doctor]:
        expressions = self.get_search_expressions(search)
        statement = (
            (
                select(self.model)
                .filter_by(**filters)
                .where(*expressions)
                .options(
                    joinedload(self.model.speciality), joinedload(self.model.department)
                )
            )
            .limit(limit)
            .offset(offset)
            .order_by(self.model.id)
        )
        res = await self.session.execute(statement)
        return res.scalars().all()

    async def get_with_relations(self, id: int) -> Doctor | None:
        options = [
            joinedload(self.model.speciality),
            joinedload(self.model.department),
            selectinload(self.model.education),
            selectinload(self.model.extra_education),
            selectinload(self.model.inspections),
            with_expression(
                self.model.experience_years,
                select(func.extract("year", func.now()) - self.model.experience_start)
                .where(Doctor.id == self.model.id)
                .correlate(Doctor)
                .scalar_subquery(),
            ),
        ]
        statement = select(self.model).where(self.model.id == id).options(*options)
        res = await self.session.execute(statement)
        return res.scalar_one_or_none()

    async def create(self, data: dict) -> Doctor:
        inspections = data.pop("inspections", [])
        education = data.pop("education", [])
        extra_education = data.pop("extra_education", [])

        instance = self.model(**data)
        instance.doctor_inspections = [
            DoctorInspection(**inspection) for inspection in inspections
        ]
        instance.education = [Education(title=title) for title in education]
        instance.extra_education = [
            ExtraEducation(title=title) for title in extra_education
        ]
        self.session.add(instance)
        try:
            await self.session.commit()
        except IntegrityError as ex:
            await self.handle_error(ex)
        else:
            doctor = await self.get_with_relations(instance.id)
            if not doctor:
                raise DoctorWasDeletedError
            return doctor

    async def update(
        self,
        id: int,
        data: dict,
    ) -> Doctor | None:
        inspections: list[dict] | None = data.pop("inspections", None)
        education: list[str] | None = data.pop("education", None)
        extra_education: list[str] | None = data.pop("extra_education", None)

        instance = await self.get_with_relations(id)
        if not instance:
            return None

        if education is not None:
            instance.education = [Education(title=title) for title in education]
        if extra_education is not None:
            instance.extra_education = [
                ExtraEducation(title=title) for title in extra_education
            ]
        if inspections is not None:
            await instance.awaitable_attrs.doctor_inspections
            instance.doctor_inspections = [
                DoctorInspection(**inspection) for inspection in inspections
            ]
        for attr in data:
            setattr(instance, attr, data[attr])
        try:
            await self.session.commit()
        except IntegrityError as ex:
            await self.handle_error(ex)
        else:
            self.session.expire(instance)
            doctor = await self.get_with_relations(id)
            if not doctor:
                raise DoctorWasDeletedError
            return doctor
