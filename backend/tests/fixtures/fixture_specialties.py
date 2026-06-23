import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.doctors import Speciality
from src.schemas.specialities import CreateSpecialitySchema


@pytest.fixture
def gen_speciality_payload(faker):
    def wrapper():
        return {"name": faker.unique.name()}

    return wrapper


@pytest.fixture
def create_speciality_instance(gen_speciality_payload):
    def wrapper():
        schema = CreateSpecialitySchema(**gen_speciality_payload())
        return Speciality(**schema.model_dump())

    return wrapper


@pytest_asyncio.fixture
async def speciality(session: AsyncSession, create_speciality_instance):
    instance = create_speciality_instance()
    session.add(instance)
    await session.commit()
    return instance


@pytest_asyncio.fixture
async def doctor_speciality(session: AsyncSession, create_speciality_instance):
    instance = create_speciality_instance()
    session.add(instance)
    await session.commit()
    return instance


@pytest_asyncio.fixture
async def specialties(session: AsyncSession, create_speciality_instance):
    instances = [create_speciality_instance() for _ in range(10)]
    session.add_all(instances)
    await session.commit()
    return instances
