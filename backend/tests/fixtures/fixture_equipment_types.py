import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.equipments import EquipmentType
from src.schemas.equipments import CreateEquipmentTypeSchema


@pytest.fixture
def gen_equipment_type_payload(faker):
    def wrapper():
        return {"name": faker.unique.name()}

    return wrapper


@pytest.fixture
def create_equipment_type_instance(gen_equipment_type_payload):
    def wrapper():
        schema = CreateEquipmentTypeSchema(**gen_equipment_type_payload())
        return EquipmentType(**schema.model_dump())

    return wrapper


@pytest_asyncio.fixture
async def equipment_type(session: AsyncSession, create_equipment_type_instance):
    instance = create_equipment_type_instance()
    session.add(instance)
    await session.commit()
    return instance


@pytest_asyncio.fixture
async def other_equipment_type(session: AsyncSession, create_equipment_type_instance):
    instance = create_equipment_type_instance()
    session.add(instance)
    await session.commit()
    return instance


@pytest_asyncio.fixture
async def related_equipment_type(session: AsyncSession, create_equipment_type_instance):
    instance = create_equipment_type_instance()
    session.add(instance)
    await session.commit()
    return instance


@pytest_asyncio.fixture
async def equipment_types(session: AsyncSession, create_equipment_type_instance):
    instances = [create_equipment_type_instance() for _ in range(10)]
    session.add_all(instances)
    await session.commit()
    return instances
