import asyncio

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database.core import AsyncSessionLocal
from src.models.doctors import Department, Doctor, Speciality
from src.models.inspections import Inspection # noqa


def fill_specialities(session: Session):
    instance = Speciality(name="Врач-рентгенолог")
    session.add(instance)
    session.commit()


def fill_departments(session: Session):
    instance = Department(
        name="Отделение ультразвуковой диагностики и рентгенодиагностики"
    )
    session.add(instance)
    session.commit()


def fill_doctors(session: Session):
    instance = Doctor(
        firstname="Иван",
        lastname="Иванов",
        middlename="Иванович",
        qualification="Высшая квалификационная категория",
        experience_start=2000,
        speciality_id=1,
        department_id=1,
    )
    session.add(instance)
    session.commit()


async def main():
    async with AsyncSessionLocal() as session:
        try:
            await session.run_sync(fill_departments)
            await session.run_sync(fill_specialities)
            # await session.run_sync(fill_doctors)
            print("data inserted")
        except IntegrityError:
            await session.rollback()
            print("integrity error")
        finally:
            await session.close()


if __name__ == "__main__":
    asyncio.run(main())
