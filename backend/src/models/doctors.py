from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, query_expression, relationship

from src.database.core import Base as RawBase
from src.models.mixins import IntPkBase as Base

if TYPE_CHECKING:
    from src.models.inspections import Inspection


class DoctorInspection(RawBase):
    __tablename__ = "doctor_inspections"

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id", ondelete="CASCADE"), primary_key=True
    )
    inspection_id: Mapped[int] = mapped_column(
        ForeignKey("inspections.id", ondelete="CASCADE"), primary_key=True
    )

    doctor: Mapped["Doctor"] = relationship(back_populates="doctor_inspections")
    inspection: Mapped["Inspection"] = relationship(back_populates="inspection_doctors")


class Doctor(Base):
    __tablename__ = "doctors"

    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    middlename: Mapped[str] = mapped_column(String(50))

    qualification: Mapped[str | None] = mapped_column(String(255))
    experience_start: Mapped[int | None]
    photo: Mapped[str | None] = mapped_column(server_default=None)

    speciality_id: Mapped[int] = mapped_column(ForeignKey("specialities.id"))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))

    speciality: Mapped["Speciality"] = relationship(back_populates="doctors")
    department: Mapped["Department"] = relationship(back_populates="doctors")
    education: Mapped[list["Education"]] = relationship(cascade="all, delete-orphan")
    extra_education: Mapped[list["ExtraEducation"]] = relationship(
        cascade="all, delete-orphan"
    )

    doctor_inspections: Mapped[list["DoctorInspection"]] = relationship(
        back_populates="doctor",
        cascade="all, delete-orphan",
    )

    inspections: Mapped[list["Inspection"]] = relationship(
        secondary="doctor_inspections", back_populates="doctors", viewonly=True
    )

    experience_years = query_expression()

    __table_args__ = (
        CheckConstraint(
            "experience_start >= 1920 AND experience_start <= EXTRACT(YEAR FROM CURRENT_DATE)",
            name="check_experience_start",
        ),
    )


class Education(RawBase):
    __tablename__ = "education"

    title: Mapped[str] = mapped_column(String(255), primary_key=True)
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey(Doctor.id, ondelete="CASCADE"), primary_key=True
    )


class ExtraEducation(RawBase):
    __tablename__ = "extra_education"

    title: Mapped[str] = mapped_column(String(255), primary_key=True)
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey(Doctor.id, ondelete="CASCADE"), primary_key=True
    )


class Speciality(Base):
    __tablename__ = "specialities"

    name: Mapped[str] = mapped_column(String(255), unique=True)

    doctors: Mapped[list["Doctor"]] = relationship(back_populates="speciality")


class Department(Base):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(String(255), unique=True)

    doctors: Mapped[list["Doctor"]] = relationship(back_populates="department")
