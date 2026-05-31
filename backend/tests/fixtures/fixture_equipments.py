import pytest_asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.equipments import Equipment, EquipmentType
from src.schemas.equipments import CreateEquipmentSchema

faker = Faker()


@pytest_asyncio.fixture
async def gen_equipment_data(related_equipment_type: EquipmentType, image_url: str):
    async def wrapper():
        return {
            "name": faker.name(),
            "image": image_url,
            "type_id": related_equipment_type.id,
        }

    return wrapper


@pytest_asyncio.fixture
async def create_equipment_instance(gen_equipment_data):
    async def wrapper():
        schema = CreateEquipmentSchema(**await gen_equipment_data())
        return Equipment(**schema.model_dump(mode="json"))

    return wrapper


@pytest_asyncio.fixture
async def equipment(session: AsyncSession, create_equipment_instance):
    instance = await create_equipment_instance()
    session.add(instance)
    await session.commit()
    return instance


@pytest_asyncio.fixture
async def equipments(session: AsyncSession, create_equipment_instance):
    instance = [await create_equipment_instance() for _ in range(10)]
    session.add(instance)
    await session.commit()
    return instance
