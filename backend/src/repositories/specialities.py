from src.models.doctors import Speciality
from src.repositories.base import DefaultRepository


class SpecialitiesRepository(DefaultRepository[Speciality]):
    model = Speciality

    async def create(self, data: dict) -> Speciality:
        research = Speciality(**data)
        self.session.add(research)
        await self.session.commit()
        await self.session.refresh(research)
        return research
