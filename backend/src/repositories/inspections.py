from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from models.inspections import Inspection
from src.repositories.base import DefaultRepository


class InspectionRepository(DefaultRepository[Inspection]):
    model = Inspection
    options = (joinedload(model.doctor),)

    async def get_with_relations(self, id: int) -> Inspection | None:
        return await self.session.get(self.model, id, options=self.options)

    async def get_all_with_relations(self) -> Sequence[Inspection]:
        statement = select(self.model).options(*self.options)
        res = await self.session.execute(statement)
        return res.scalars().all()

    async def create(self, data: dict) -> Inspection | None:
        instance = self.model(**data)
        self.session.add(instance)
        try:
            await self.session.commit()
        except IntegrityError:
            return None
        await self.session.refresh(instance, attribute_names=("doctor",))
        return instance
