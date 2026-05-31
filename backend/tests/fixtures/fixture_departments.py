import pytest
import pytest_asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.doctors import Department
from src.schemas.departments import CreateDepartmentSchema

faker = Faker()


@pytest.fixture
def gen_department_payload():
    def wrapper():
        return {"name": faker.name()}

    return wrapper


@pytest.fixture
def create_department_instance(gen_department_payload):
    def wrapper():
        schema = CreateDepartmentSchema(**gen_department_payload())
        return Department(**schema.model_dump())

    return wrapper


@pytest_asyncio.fixture
async def department(session: AsyncSession, create_department_instance):
    instance = create_department_instance()
    session.add(instance)
    await session.commit()
    return instance


@pytest_asyncio.fixture
async def doctor_department(session: AsyncSession, create_department_instance):
    instance = create_department_instance()
    session.add(instance)
    await session.commit()
    return instance


@pytest_asyncio.fixture
async def departments(session: AsyncSession, create_department_instance):
    instances = [create_department_instance() for _ in range(10)]
    session.add_all(instances)
    await session.commit()
    return instances
