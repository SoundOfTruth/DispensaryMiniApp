from typing import Annotated

from fastapi import Depends

from src.api.exceptions import NotFoundException
from src.database.core import AsyncScopedSessionDep
from src.repositories.specialities import SpecialitiesRepository
from src.schemas.specialities import CreateSpecialitySchema, SpecialitySchema


class SpecialityService:
    def __init__(self, session: AsyncScopedSessionDep):
        self.specialitie_rep = SpecialitiesRepository(session)

    async def get(self, id: int) -> SpecialitySchema:
        speciality = await self.specialitie_rep.get(id)
        if not speciality:
            raise NotFoundException
        return SpecialitySchema.model_validate(speciality)

    async def get_all(self) -> list[SpecialitySchema]:
        specialities = await self.specialitie_rep.get_all()
        return [
            SpecialitySchema.model_validate(speciality) for speciality in specialities
        ]

    async def create(self, schema: CreateSpecialitySchema) -> SpecialitySchema:
        payload = schema.model_dump()
        speciality = await self.specialitie_rep.create(payload)
        return SpecialitySchema.model_validate(speciality)


SpecialityServiceDep = Annotated[SpecialityService, Depends(SpecialityService)]
