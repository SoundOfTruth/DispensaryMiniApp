import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.doctors import Department, Doctor, Speciality


@pytest.fixture
def gen_doctor_payload(faker):
    def wrapper(specality_id: int, department_id: int, photo: str | None = None):
        return {
            "photo": photo,
            "firstname": faker.first_name(),
            "lastname": faker.last_name(),
            "middlename": faker.first_name(),
            "qualification": faker.name(),
            "experience_start": 2000,
            "speciality_id": specality_id,
            "department_id": department_id,
            "education": [],
            "extra_education": [],
            "inspections": [],
        }

    return wrapper


@pytest.fixture
def create_doctor_instance(gen_doctor_payload):
    def wrapper(specality_id: int, department_id: int, photo: str | None = None):
        payload = gen_doctor_payload(specality_id, department_id, photo)
        payload.pop("education")
        payload.pop("extra_education")
        payload.pop("inspections")
        return Doctor(**payload)

    return wrapper


@pytest_asyncio.fixture
async def doctor(
    session: AsyncSession,
    create_doctor_instance,
    doctor_speciality: Speciality,
    doctor_department: Department,
):
    instance = create_doctor_instance(doctor_speciality.id, doctor_department.id)
    session.add(instance)
    await session.commit()
    return instance


@pytest_asyncio.fixture
async def doctors(
    session: AsyncSession,
    create_doctor_instance,
    doctor_speciality: Speciality,
    doctor_department: Department,
):
    instances = [
        create_doctor_instance(doctor_speciality.id, doctor_department.id)
        for _ in range(10)
    ]
    session.add_all(instances)
    await session.commit()
    return instances


@pytest_asyncio.fixture
async def doctors_real_photo(
    session: AsyncSession,
    create_doctor_instance,
    doctor_speciality: Speciality,
    doctor_department: Department,
    create_temp_files,
):
    files = create_temp_files(10)
    instances = [
        create_doctor_instance(doctor_speciality.id, doctor_department.id, file)
        for file in files
    ]
    session.add_all(instances)
    await session.commit()
    return instances


@pytest_asyncio.fixture
async def many_doctors(
    session: AsyncSession,
    create_doctor_instance,
    doctor_speciality: Speciality,
    doctor_department: Department,
):
    instances = [
        create_doctor_instance(doctor_speciality.id, doctor_department.id)
        for _ in range(50)
    ]
    session.add_all(instances)
    await session.commit()
    return instances
