import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.doctors import Doctor, DoctorInspection
from src.models.inspections import Inspection


@pytest.fixture
def gen_inspection_payload(faker):
    def wrapper():
        return {
            "title": faker.unique.name(),
            "description": faker.text(),
            "preparation": faker.text(),
            "doctors": [],
        }

    return wrapper


@pytest.fixture
def create_inspection_instance(gen_inspection_payload):
    def wrapper():
        payload: dict = gen_inspection_payload()
        payload.pop("doctors", [])
        return Inspection(**gen_inspection_payload())

    return wrapper


@pytest_asyncio.fixture
async def inspection(
    session: AsyncSession,
    create_inspection_instance,
):
    instance = create_inspection_instance()
    session.add(instance)
    await session.commit()
    return instance


@pytest_asyncio.fixture
async def other_inspection(
    session: AsyncSession,
    create_inspection_instance,
):
    instance = create_inspection_instance()
    session.add(instance)
    await session.commit()
    return instance


@pytest_asyncio.fixture
async def inspections(
    session: AsyncSession,
    create_inspection_instance,
):
    instances = [create_inspection_instance() for _ in range(10)]
    session.add_all(instances)
    await session.commit()
    return instances


@pytest_asyncio.fixture
async def inspection_with_doctors(
    session: AsyncSession, create_inspection_instance, doctors: list[Doctor]
):
    instance: Inspection = create_inspection_instance()
    instance.inspection_doctors = [
        DoctorInspection(doctor_id=doctor.id) for doctor in doctors
    ]
    session.add(instance)
    await session.commit()
    return instance


@pytest_asyncio.fixture
async def many_inspections(
    session: AsyncSession,
    create_inspection_instance,
):
    instances = [create_inspection_instance() for _ in range(50)]
    session.add_all(instances)
    await session.commit()
    return instances
