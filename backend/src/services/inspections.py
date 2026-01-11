from typing import Annotated

from fastapi import Depends

from src.api.exceptions import NotFoundException
from src.database.core import AsyncScopedSessionDep
from src.repositories.inspections import InspectionRepository
from src.schemas.inspections import CreateInspectionSchema, InspectionSchema


class InspectionService:
    def __init__(self, session: AsyncScopedSessionDep):
        self.inspetion_rep = InspectionRepository(session)

    async def get(self, id: int):
        inspection = await self.inspetion_rep.get_with_relations(id)
        if not inspection:
            raise NotFoundException
        return InspectionSchema.model_validate(inspection)

    async def get_all(self):
        inspections = await self.inspetion_rep.get_all_with_relations()
        return [
            InspectionSchema.model_validate(inspection) for inspection in inspections
        ]

    async def create(self, schema: CreateInspectionSchema):
        payload = schema.model_dump()
        doctors = payload.pop("doctors")
        inspection = await self.inspetion_rep.create(payload, doctors)
        return InspectionSchema.model_validate(inspection)


InspectionServiceDep = Annotated[InspectionService, Depends(InspectionService)]
