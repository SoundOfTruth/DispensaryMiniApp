from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.core import Base
from src.models.types import int_pk


class Equipment(Base):
    __tablename__ = "equipments"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(255), unique=True)
    image: Mapped[str | None] = mapped_column(server_default=None)
