from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from src.api.exceptions import DbIntegrityException
from src.models import Doctor, DoctorInspection, Inspection
from src.repositories.base import DefaultRepository


class InspectionRepository(DefaultRepository[Inspection]):
    model = Inspection
    options = (
        selectinload(model.doctors).joinedload(Doctor.speciality),
        selectinload(model.doctors).joinedload(Doctor.department),
    )

    async def get_with_relations(self, id: int) -> Inspection | None:
        statement = select(self.model).where(self.model.id == id).options(*self.options)
        res = await self.session.execute(statement)
        return res.scalar_one_or_none()

    async def get_all_with_relations(self) -> Sequence[Inspection]:
        statement = select(self.model).options(*self.options)
        res = await self.session.execute(statement)
        return res.scalars().all()

    async def create(self, data: dict, doctors: list[dict]) -> Inspection | None:
        instance = self.model(**data)
        self.session.add(instance)
        try:
            await self.session.commit()
            await self.session.flush()
            inspection_id = instance.id
            self.session.add_all(
                [
                    DoctorInspection(
                        doctor_id=doctor["id"], inspection_id=inspection_id
                    )
                    for doctor in doctors
                ]
            )
            await self.session.commit()
        except IntegrityError as ex:
            message = "Непредвиденная ошибка"
            params = ex.params
            ids = list(map(lambda x: x[0], params)) if params else [] # type: ignore
            if 'отсутствует в таблице "doctors"' in str(ex.orig) and params:
                message = f"Врач(и) с id {ids} не в базе данных."
            raise DbIntegrityException(detail=message)
        return await self.get_with_relations(instance.id)
