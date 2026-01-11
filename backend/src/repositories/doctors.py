from typing import Sequence

from sqlalchemy import func, select
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

    async def get_all(self) -> Sequence[Doctor]:
        statement = select(self.model).options(
            joinedload(self.model.speciality), joinedload(self.model.department)
        )
        res = await self.session.execute(statement)
        return res.scalars().all()

    async def get_with_relations(self, id: int) -> Doctor | None:
        return await self.session.get(self.model, id, options=self.options)

    async def get_all_with_relations(self) -> Sequence[Doctor]:
        statement = select(self.model).options(*self.options)
        res = await self.session.execute(statement)
        return res.scalars().all()

    async def create(
        self, data: dict, education: list[str], extra_education: list[str]
    ) -> Doctor:
        instance = self.model(**data)
        instance.education = [Education(title=title) for title in education]
        instance.extra_education = [
            ExtraEducation(title=title) for title in extra_education
        ]
        self.session.add(instance)
        try:
            await self.session.commit()
        except IntegrityError as ex:
            print(ex)
            raise DbIntegrityException(detail="Ошибка")
        await self.session.refresh(instance)
        doctor_id = instance.id
        doctor = await self.get_with_relations(doctor_id)
        return doctor
