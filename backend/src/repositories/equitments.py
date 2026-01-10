from src.models.equipments import Equipment
from src.repositories.base import DefaultRepository


class EquipmentRepository(DefaultRepository[Equipment]):
    model = Equipment

    async def create(self, data: dict) -> Equipment:
        research = Equipment(**data)
        self.session.add(research)
        await self.session.commit()
        await self.session.refresh(research)
        return research
