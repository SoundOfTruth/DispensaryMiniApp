from typing import Annotated

from fastapi import Depends

from src.cache.manager import CacheManager
from src.database.core import AsyncScopedSessionDep
from src.repositories.specialities import SpecialityRepository
from src.schemas.specialities import (
    CreateSpecialitySchema,
    SpecialitySchema,
    UpdateSpecialitySchema,
)
from src.services.exceptions import NotFoundError

cache = CacheManager("speciality")


class SpecialityService:
    def __init__(self, session: AsyncScopedSessionDep):
        self.speciality_rep = SpecialityRepository(session)

    @cache.expire
    async def create(self, schema: CreateSpecialitySchema) -> SpecialitySchema:
        payload = schema.model_dump()
        speciality = await self.speciality_rep.create(payload)
        return SpecialitySchema.model_validate(speciality)

    @cache.expire
    async def update(self, id: int, schema: UpdateSpecialitySchema) -> SpecialitySchema:
        speciality = await self.speciality_rep.update(id, schema.model_dump())
        if not speciality:
            raise NotFoundError
        return SpecialitySchema.model_validate(speciality)

    @cache.use
    async def get_all(self, search: str | None) -> list[SpecialitySchema]:
        specialities = await self.speciality_rep.get_all(search=search)
        return [
            SpecialitySchema.model_validate(speciality) for speciality in specialities
        ]

    @cache.use
    async def get(self, id: int) -> SpecialitySchema:
        speciality = await self.speciality_rep.get(id)
        if not speciality:
            raise NotFoundError
        return SpecialitySchema.model_validate(speciality)

    @cache.expire
    async def delete(self, id: int):
        return await self.speciality_rep.delete(id)


SpecialityServiceDep = Annotated[SpecialityService, Depends()]
