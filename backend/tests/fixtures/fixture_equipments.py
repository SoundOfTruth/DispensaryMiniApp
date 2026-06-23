import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.equipments import Equipment, EquipmentType
from src.schemas.equipments import CreateEquipmentSchema


@pytest.fixture
def gen_equipment_payload(image_url: str, faker):
    def wrapper(equipment_type_id: int):
        return {
            "name": faker.unique.name(),
            "image": image_url,
            "type_id": equipment_type_id,
        }

    return wrapper


@pytest.fixture
def create_equipment_instance(gen_equipment_payload):
    def wrapper(equipment_type_id: int):
        payload = gen_equipment_payload(equipment_type_id)
        try:
            schema = CreateEquipmentSchema(**payload)
            return Equipment(**schema.model_dump(mode="json"))
        except Exception as ex:
            print(ex)

    return wrapper


@pytest_asyncio.fixture
async def equipment(
    session: AsyncSession,
    create_equipment_instance,
    related_equipment_type: EquipmentType,
):
    instance = create_equipment_instance(related_equipment_type.id)
    session.add(instance)
    await session.commit()
    return instance


@pytest_asyncio.fixture
async def other_equipment(
    session: AsyncSession,
    create_equipment_instance,
    related_equipment_type: EquipmentType,
):
    instance = create_equipment_instance(related_equipment_type.id)
    session.add(instance)
    await session.commit()
    return instance


@pytest_asyncio.fixture
async def equipments(
    session: AsyncSession,
    create_equipment_instance,
    related_equipment_type: EquipmentType,
):
    instance = [create_equipment_instance(related_equipment_type.id) for _ in range(10)]
    session.add_all(instance)
    await session.commit()
    return instance
