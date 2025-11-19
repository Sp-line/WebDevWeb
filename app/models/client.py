from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from app.models import Person
from app.models.mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from app.models.order import Order


class Client(IdIntPkMixin, Person):
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="client")

    def __str__(self) -> str:
        return f"<Client: {self.email}>"
