from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.core import Base
from src.models.types import int_pk

if TYPE_CHECKING:
    from src.models.doctors import Doctor


class DoctorInspection(Base):
    __tablename__ = "doctor_inspections"

    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"), primary_key=True)
    inspection_id: Mapped[int] = mapped_column(
        ForeignKey("inspections.id"), primary_key=True
    )


class Inspection(Base):
    __tablename__ = "inspections"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(Text())
    preparation: Mapped[str] = mapped_column(Text())

    doctors: Mapped[list["Doctor"]] = relationship(
        "Doctor", secondary="doctor_inspections", back_populates="inspections"
    )
