import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Department, Speciality
from src.repositories.departments import DepartmentRepository
from src.repositories.doctors import DoctorRepository
from src.repositories.specialities import SpecialityRepository
from tests.core import TestAsyncSessionLocal


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def session(anyio_backend):
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture
async def department(session: AsyncSession):
    repository = DepartmentRepository(session)
    payload = {"name": "Отделение 1"}
    yield await repository.create(payload)


@pytest.fixture
async def speciality(session: AsyncSession):
    repository = SpecialityRepository(session)
    payload = {"name": "Врач-рентгенолог"}
    yield await repository.create(payload)


@pytest.fixture
async def doctor(session: AsyncSession, speciality: Speciality, department: Department):
    repository = DoctorRepository(session)
    data = {
        "firstname": "test1",
        "lastname": "test2",
        "middlename": "test3",
        "photo": None,
        "speciality_id": speciality.id,
        "department_id": department.id,
        "education": ["test_edu_1", "test_edu_2"],
        "extra_education": ["test_extra_1", "test_extra_2"],
    }
    yield await repository.create(data)
