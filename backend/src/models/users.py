from enum import Enum

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.mixins import IntPkBase as Base


class Role(Enum):
    superuser = "superuser"
    admin = "admin"
    user = "user"


roles = tuple(role.value for role in Role)
roles = ("superuser", "admin", "user").__str__()


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(254), unique=True)
    lastname: Mapped[str] = mapped_column(String(50))
    firstname: Mapped[str] = mapped_column(String(50))
    middlename: Mapped[str] = mapped_column(String(50))
    password: Mapped[str]

    role: Mapped[str] = mapped_column(String(20), server_default=Role.user.value)

    __table_args__ = (
        CheckConstraint(
            f"role IN {roles}",
            name="check_role",
        ),
    )
