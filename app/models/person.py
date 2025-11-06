from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class Person(Base):
    __abstract__ = True

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)