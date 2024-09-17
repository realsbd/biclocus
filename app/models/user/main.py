from sqlalchemy import JSON
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.functions.hash import check_hash, get_hash
from app.models.auth.role import Role
from app.models.post import Post


class User(AsyncAttrs, Base):
    __tablename__ = "user"
    firstName: Mapped[str] = mapped_column(nullable=True)
    lastName: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True)
    _password: Mapped[str] = mapped_column(name="password")
    username: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(nullable=True)
    date_of_birth: Mapped[str] = mapped_column(nullable=True)
    avatar: Mapped[str] = mapped_column(nullable=True)
    level: Mapped[str] = mapped_column(nullable=True)
    cgpa: Mapped[str] = mapped_column(nullable=True)
    matric_number: Mapped[str] = mapped_column(nullable=True)
    institution: Mapped[str] = mapped_column(nullable=True)
    faculty: Mapped[str] = mapped_column(nullable=True)
    department: Mapped[str] = mapped_column(nullable=True)
    verified: Mapped[bool] = mapped_column(default=False)
    scope: Mapped[list[Role]] = mapped_column(JSON, nullable=False, default=[Role.USER])
    posts: Mapped[list[Post]] = relationship(
        back_populates="user", lazy="select", cascade="all, delete-orphan"
    )

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        self._password = get_hash(password)

    def check_password(self, password: str) -> bool:
        return check_hash(password, self.password)
