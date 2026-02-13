from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.core import Base
from src.models.types import int_pk


class Equipment(Base):
    __tablename__ = "equipments"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(255), unique=True)
    image: Mapped[str | None] = mapped_column(server_default=None)

    type: Mapped["EquipmentType"] = relationship(back_populates="equipments")

    type_id: Mapped[int] = mapped_column(ForeignKey("equipment_types.id"))


class EquipmentType(Base):
    __tablename__ = "equipment_types"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(255), unique=True)

    equipments: Mapped[list[Equipment]] = relationship(back_populates="type")
