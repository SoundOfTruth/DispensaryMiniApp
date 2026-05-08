from typing import Annotated

from fastapi import Depends

from src.database.core import AsyncScopedSessionDep
from src.repositories.inspections import InspectionRepository
from src.schemas.inspections import (
    CreateInspectionSchema,
    InspectionSchema,
    PaginatedInspectionSchema,
    SimpleInspectionSchema,
    UpdateInspectionSchema,
)
from src.services.exceptions import EmptyPatchError, NotFoundError


class InspectionService:
    def __init__(self, session: AsyncScopedSessionDep):
        self.inspetion_rep = InspectionRepository(session)

    async def create(self, schema: CreateInspectionSchema):
        inspection = await self.inspetion_rep.create(schema.model_dump())
        return InspectionSchema.model_validate(inspection)

    async def update(self, id: int, schema: UpdateInspectionSchema):
        payload = schema.model_dump(exclude_unset=True)
        if not payload:
            raise EmptyPatchError
        inspection = await self.inspetion_rep.update(id, payload)
        if not inspection:
            raise NotFoundError
        return InspectionSchema.model_validate(inspection)

    async def get_all(self, limit: int, offset: int, search: str | None):
        count = await self.inspetion_rep.count(search)
        inspections = await self.inspetion_rep.get_all(
            search=search, limit=limit, offset=offset
        )
        results = [
            SimpleInspectionSchema.model_validate(inspection)
            for inspection in inspections
        ]
        return PaginatedInspectionSchema(count=count, results=results)

    async def get(self, id: int):
        inspection = await self.inspetion_rep.get_with_relations(id)
        if not inspection:
            raise NotFoundError
        return InspectionSchema.model_validate(inspection)

    async def delete(self, id: int):
        return await self.inspetion_rep.delete(id)

    async def bulk_delete(self, ids: list[int]):
        return await self.inspetion_rep.bulk_delete(ids)


InspectionServiceDep = Annotated[InspectionService, Depends()]
