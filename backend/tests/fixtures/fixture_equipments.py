import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.equipments import Equipment, EquipmentType
from src.schemas.equipments import CreateEquipmentSchema
from tests.utils import gen_image_url


@pytest.fixture
def gen_equipment_payload(faker):
    def wrapper(equipment_type_id: int, image: str = gen_image_url()):
        return {
            "name": faker.unique.name(),
            "image": image,
            "type_id": equipment_type_id,
        }

    return wrapper


@pytest.fixture
def create_equipment_instance(gen_equipment_payload):
    def wrapper(equipment_type_id: int, image: str = gen_image_url()):
        payload = gen_equipment_payload(equipment_type_id, image)
        schema = CreateEquipmentSchema(**payload)
        return Equipment(**schema.model_dump(mode="json"))

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
    image_url: str,
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
    image_url: str,
    related_equipment_type: EquipmentType,
):
    instances = [
        create_equipment_instance(related_equipment_type.id) for _ in range(10)
    ]
    session.add_all(instances)
    await session.commit()
    return instances


@pytest_asyncio.fixture
async def equipments_real_image(
    session: AsyncSession,
    create_equipment_instance,
    related_equipment_type: EquipmentType,
    create_temp_files,
):
    files = create_temp_files(10)
    instances = [
        create_equipment_instance(related_equipment_type.id, file) for file in files
    ]
    session.add_all(instances)
    await session.commit()
    return instances
