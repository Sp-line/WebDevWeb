from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column


class IdIntPkMixin:
    if TYPE_CHECKING:
        id: int
    else:
        id: Mapped[int] = mapped_column(primary_key=True)
