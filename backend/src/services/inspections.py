from typing import Annotated

from fastapi import Depends

from src.cache.manager import CacheManager
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

cache = CacheManager("inspection")


class InspectionService:
    def __init__(self, session: AsyncScopedSessionDep):
        self.inspetion_rep = InspectionRepository(session)

    @cache.expire
    async def create(self, schema: CreateInspectionSchema) -> InspectionSchema:
        inspection = await self.inspetion_rep.create(schema.model_dump())
        return InspectionSchema.model_validate(inspection)

    @cache.expire
    async def update(self, id: int, schema: UpdateInspectionSchema) -> InspectionSchema:
        payload = schema.model_dump(exclude_unset=True)
        if not payload:
            raise EmptyPatchError
        inspection = await self.inspetion_rep.update(id, payload)
        if not inspection:
            raise NotFoundError
        return InspectionSchema.model_validate(inspection)

    @cache.use
    async def get_all(
        self, limit: int, offset: int, search: str | None, filled: bool
    ) -> PaginatedInspectionSchema:
        count = await self.inspetion_rep.count(search, filled)
        inspections = await self.inspetion_rep.get_all(
            search=search, limit=limit, offset=offset, filled=filled
        )
        results = [
            SimpleInspectionSchema.model_validate(inspection)
            for inspection in inspections
        ]
        return PaginatedInspectionSchema(count=count, results=results)

    @cache.use
    async def get(self, id: int) -> InspectionSchema:
        inspection = await self.inspetion_rep.get_with_relations(id)
        if not inspection:
            raise NotFoundError
        return InspectionSchema.model_validate(inspection)

    @cache.expire
    async def delete(self, id: int):
        return await self.inspetion_rep.delete(id)


InspectionServiceDep = Annotated[InspectionService, Depends()]
