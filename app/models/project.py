from datetime import datetime

from sqlalchemy import DateTime, String, Text, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from models import Base
from models.mixins.id_int_pk import IdIntPkMixin


class Project(IdIntPkMixin, Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now())
    end_date: Mapped[datetime | None] = mapped_column(DateTime)

    order: Mapped["Order"] = relationship("Order", back_populates="project", uselist=False)
    teams: Mapped[list["Team"]] = relationship("Team", back_populates="project")

    __table_args__ = (
        CheckConstraint(
            "start_date IS NULL OR end_date IS NULL OR end_date >= start_date",
            name="ck_project_dates"
        ),
    )

    @validates("start_date", "end_date")
    def validate_dates(self, key: str, value: datetime | None) -> datetime | None:
        if key == "start_date" and value and self.end_date:
            if value > self.end_date:
                raise ValueError("Start date cannot be after end date")
        elif key == "end_date" and value and self.start_date:
            if value < self.start_date:
                raise ValueError("End date cannot be before start date")
        return value