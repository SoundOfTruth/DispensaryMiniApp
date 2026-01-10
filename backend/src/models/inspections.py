from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.core import Base
from src.models.types import int_pk

if TYPE_CHECKING:
    from src.models.doctors import Doctor


class Inspection(Base):
    __tablename__ = "inspections"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    preparation: Mapped[str] = mapped_column(String(255))

    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))

    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="inspections")
