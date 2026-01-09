from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.core import Base
from src.models.doctors import Doctor
from src.models.types import int_pk


class Inspection(Base):
    __tablename__ = "inspections"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    preparation: Mapped[str] = mapped_column(String(255))

    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))

    doctor: Mapped["Doctor"] = relationship(back_populates="inspections")
