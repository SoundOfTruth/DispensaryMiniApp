from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, query_expression, relationship

from src.database.core import Base
from src.models.types import int_pk

if TYPE_CHECKING:
    from src.models.inspections import Inspection


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int_pk]
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    middlename: Mapped[str] = mapped_column(String(50))
    qualification: Mapped[str | None] = mapped_column(String(255))
    experience_start: Mapped[int | None]

    experience = query_expression()

    education: Mapped[list["Education"]] = relationship()
    extra_education: Mapped[list["ExtraEducation"]] = relationship()

    speciality: Mapped["Speciality"] = relationship(back_populates="doctors")
    department: Mapped["Department"] = relationship(back_populates="doctors")
    inspections: Mapped[list["Inspection"]] = relationship(
        "Inspection", back_populates="doctor"
    )

    speciality_id: Mapped[int] = mapped_column(ForeignKey("specialities.id"))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))

    __table_args__ = (
        CheckConstraint(
            "experience_start >= 1920",
            name="check_experience_start",
        ),
    )  # for porgresql experience_start >= 1920 AND eexperience_start <= EXTRACT(YEAR FROM CURRENT_DATE)


class Education(Base):
    __tablename__ = "education"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(255))

    doctor_id: Mapped[int] = mapped_column(ForeignKey(Doctor.id))


class ExtraEducation(Base):
    __tablename__ = "extra_education"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(255))

    doctor_id: Mapped[int] = mapped_column(ForeignKey(Doctor.id))


class Speciality(Base):
    __tablename__ = "specialities"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(255), unique=True)

    doctors: Mapped[list["Doctor"]] = relationship(back_populates="speciality")


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(255), unique=True)

    doctors: Mapped[list["Doctor"]] = relationship(back_populates="department")
