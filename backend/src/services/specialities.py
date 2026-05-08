from typing import Annotated

from fastapi import Depends

from src.database.core import AsyncScopedSessionDep
from src.repositories.specialities import SpecialityRepository
from src.schemas.specialities import (
    CreateSpecialitySchema,
    SpecialitySchema,
    UpdateSpecialitySchema,
)
from src.services.exceptions import NotFoundError


class SpecialityService:
    def __init__(self, session: AsyncScopedSessionDep):
        self.speciality_rep = SpecialityRepository(session)

    async def create(self, schema: CreateSpecialitySchema) -> SpecialitySchema:
        payload = schema.model_dump()
        speciality = await self.speciality_rep.create(payload)
        return SpecialitySchema.model_validate(speciality)

    async def update(self, id: int, schema: UpdateSpecialitySchema):
        speciality = await self.speciality_rep.update(id, schema.model_dump())
        if not speciality:
            raise NotFoundError
        return SpecialitySchema.model_validate(speciality)

    async def get_all(self) -> list[SpecialitySchema]:
        specialities = await self.speciality_rep.get_all()
        return [
            SpecialitySchema.model_validate(speciality) for speciality in specialities
        ]

    async def get(self, id: int) -> SpecialitySchema:
        speciality = await self.speciality_rep.get(id)
        if not speciality:
            raise NotFoundError
        return SpecialitySchema.model_validate(speciality)

    async def delete(self, id: int):
        return await self.speciality_rep.delete(id)

    async def bulk_delete(self, ids: list[int]):
        return await self.speciality_rep.bulk_delete(ids)


SpecialityServiceDep = Annotated[SpecialityService, Depends()]
