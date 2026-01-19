from sqlalchemy.exc import IntegrityError

from src.api.exceptions import DbIntegrityException
from src.models.doctors import Department
from src.repositories.base import DefaultRepository


class DepartmentRepository(DefaultRepository[Department]):
    model = Department

    async def create(self, data: dict) -> Department:
        research = Department(**data)
        self.session.add(research)
        try:
            await self.session.commit()
        except IntegrityError:
            raise DbIntegrityException(detail="Отделение уже сушествует")
        await self.session.refresh(research)
        return research
