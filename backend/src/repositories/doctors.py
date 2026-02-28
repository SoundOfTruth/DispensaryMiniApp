from typing import Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, selectinload, with_expression

from src.api.exceptions import DbIntegrityException
from src.models import Doctor, Education, ExtraEducation
from src.repositories.base import BaseRepository


class DoctorRepository(BaseRepository[Doctor]):
    model = Doctor
    options = (
        selectinload(model.education),
        selectinload(model.extra_education),
        selectinload(model.inspections),
        joinedload(model.speciality),
        joinedload(model.department),
        with_expression(
            model.experience,
            select(func.extract("year", func.now()) - model.experience_start)
            .where(Doctor.id == model.id)
            .correlate(Doctor)
            .scalar_subquery(),
        ),
    )

    async def get(self, id: int) -> Doctor | None:
        return await self.session.get(self.model, id)

    async def get_all(
        self, search: str | None, filters: dict[str, int] = {}
    ) -> Sequence[Doctor]:
        expressions = []
        if search:
            expressions.append(
                or_(
                    self.model.lastname.icontains(search),
                    self.model.firstname.icontains(search),
                    self.model.middlename.icontains(search),
                )
            )
        statement = (
            select(self.model)
            .filter_by(**filters)
            .where(*expressions)
            .options(
                joinedload(self.model.speciality), joinedload(self.model.department)
            )
        )
        res = await self.session.execute(statement)
        return res.scalars().all()

    async def get_with_relations(self, id: int) -> Doctor | None:
        statement = select(self.model).where(self.model.id == id).options(*self.options)
        res = await self.session.execute(statement)
        return res.scalar_one_or_none()

    async def get_all_with_relations(self) -> Sequence[Doctor]:
        statement = select(self.model).options(*self.options)
        res = await self.session.execute(statement)
        return res.scalars().all()

    async def create(
        self, data: dict, education: list[dict], extra_education: list[dict]
    ) -> Doctor | None:
        instance = self.model(**data)
        instance.education = [Education(title=obj["title"]) for obj in education]
        instance.extra_education = [
            ExtraEducation(title=obj["title"]) for obj in extra_education
        ]
        self.session.add(instance)
        try:
            await self.session.commit()
        except IntegrityError:
            raise DbIntegrityException(detail="Ошибка")
        await self.session.refresh(instance)
        doctor_id = instance.id
        doctor = await self.get_with_relations(doctor_id)
        return doctor
