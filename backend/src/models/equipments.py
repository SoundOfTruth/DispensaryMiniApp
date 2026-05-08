from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.mixins import IntPkBase as Base


class Equipment(Base):
    __tablename__ = "equipments"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    image: Mapped[str | None] = mapped_column(server_default=None)

    type: Mapped["EquipmentType"] = relationship(back_populates="equipments")

    type_id: Mapped[int] = mapped_column(ForeignKey("equipment_types.id"))


class EquipmentType(Base):
    __tablename__ = "equipment_types"

    name: Mapped[str] = mapped_column(String(255), unique=True)

    equipments: Mapped[list[Equipment]] = relationship(back_populates="type")
