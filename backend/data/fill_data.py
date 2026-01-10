import asyncio
import json

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database.core import AsyncSessionLocal
from src.models import Department, Doctor, Education, ExtraEducation, Speciality


def fill_specialities(session: Session):
    session.add_all(
        [
            Speciality(name="Врач-рентгенолог"),
            Speciality(name="Врач ультразвуковой диагностики"),
        ]
    )
    session.commit()


def fill_departments(session: Session):
    instance = Department(
        name="Отделение ультразвуковой диагностики и рентгенодиагностики"
    )
    session.add(instance)
    session.commit()


def fill_doctors(session: Session, data: dict):
    payload = [
        Doctor(
            firstname=doctor["firstname"],
            lastname=doctor["lastname"],
            middlename=doctor["middlename"],
            qualification=doctor["qualification"],
            experience_start=doctor["experience_start"],
            speciality_id=doctor["speciality_id"],
            department_id=doctor["department_id"],
            education=[Education(title=title) for title in doctor["education"]],
            extra_education=[
                ExtraEducation(title=title) for title in doctor["extra_education"]
            ],
        )
        for doctor in data
    ]
    session.add_all(payload)
    session.commit()


async def main():
    async with AsyncSessionLocal() as session:
        try:
            await session.run_sync(fill_departments)
            await session.run_sync(fill_specialities)
            with open("data/doctors_uzi.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            await session.run_sync(fill_doctors, data)
            with open("data/doctors_xray.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            await session.run_sync(fill_doctors, data)
            print("data inserted")
        except IntegrityError:
            await session.rollback()
            print("integrity error")
        finally:
            await session.close()


if __name__ == "__main__":
    asyncio.run(main())
