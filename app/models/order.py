from datetime import datetime

from sqlalchemy import ForeignKey, DECIMAL, DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from constants.order import TECHNICAL_TASK_MAX_LEN
from models import Base
from models.mixins.id_int_pk import IdIntPkMixin


class Order(IdIntPkMixin, Base):
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    technical_task: Mapped[str | None] = mapped_column(String(TECHNICAL_TASK_MAX_LEN), nullable=True)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    client: Mapped["Client"] = relationship("Client", back_populates="orders")
    project: Mapped["Project"] = relationship("Project", back_populates="order", uselist=False)

    @validates("created")
    def validate_created(self, key: str, value: datetime) -> datetime: # noqa: F841
        if getattr(self, "created", None) is not None:
            raise ValueError("created field cannot be modified")
        return value