from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.mixins import IntPkBase as Base

if TYPE_CHECKING:
    from src.models.doctors import Doctor, DoctorInspection


class Inspection(Base):
    __tablename__ = "inspections"

    title: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(Text())
    preparation: Mapped[str] = mapped_column(Text())

    inspection_doctors: Mapped[list["DoctorInspection"]] = relationship(
        back_populates="inspection", cascade="all, delete-orphan"
    )

    doctors: Mapped[list["Doctor"]] = relationship(
        secondary="doctor_inspections", back_populates="inspections", viewonly=True
    )
