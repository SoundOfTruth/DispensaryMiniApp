from src.models.doctors import Department
from src.repositories.base import DefaultRepository


class DepartmentRepository(DefaultRepository[Department]):
    model = Department

    async def create(self, data: dict) -> Department:
        research = Department(**data)
        self.session.add(research)
        await self.session.commit()
        await self.session.refresh(research)
        return research
