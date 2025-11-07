from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from constants.person import FIRST_NAME_MAX_LEN, LAST_NAME_MAX_LEN, EMAIL_MAX_LEN
from models import Base


class Person(Base):
    __abstract__ = True

    first_name: Mapped[str] = mapped_column(String(FIRST_NAME_MAX_LEN), nullable=False)
    last_name: Mapped[str] = mapped_column(String(LAST_NAME_MAX_LEN), nullable=False)
    email: Mapped[str] = mapped_column(String(EMAIL_MAX_LEN), unique=True, nullable=False)