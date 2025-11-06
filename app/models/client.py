from sqlalchemy.orm import Mapped, relationship

from models import Person
from models.mixins.id_int_pk import IdIntPkMixin

from models.order import Order


class Client(IdIntPkMixin, Person):
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="client")