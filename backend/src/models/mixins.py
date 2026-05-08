from sqlalchemy.orm import Mapped

from src.database.core import Base
from src.models.types import int_pk


class IntPkBase(Base):
    __abstract__ = True

    id: Mapped[int_pk]
