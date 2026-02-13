from sqlalchemy.exc import IntegrityError

from src.api.exceptions import DbIntegrityException
from src.models.doctors import Speciality
from src.repositories.base import DefaultRepository


class SpecialitiesRepository(DefaultRepository[Speciality]):
    model = Speciality

    async def create(self, data: dict) -> Speciality:
        instance = Speciality(**data)
        self.session.add(instance)
        try:
            await self.session.commit()
        except IntegrityError:
            raise DbIntegrityException(detail="Специальность уже сушествует")
        await self.session.refresh(instance)
        return instance
