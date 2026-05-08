from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.mixins import IntPkBase as Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(254), unique=True)
    lastname: Mapped[str] = mapped_column(String(50))
    firstname: Mapped[str] = mapped_column(String(50))
    middlename: Mapped[str] = mapped_column(String(50))
    password: Mapped[str]

    is_superuser: Mapped[bool] = mapped_column(server_default="false")
