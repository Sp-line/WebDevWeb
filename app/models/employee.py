import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DECIMAL, DateTime, String, ForeignKey, func, CheckConstraint, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from models import Person, Base
from models.mixins.id_int_pk import IdIntPkMixin


class GradeEnum(str, enum.Enum):
    Junior = "Junior"
    Middle = "Middle"
    Senior = "Senior"
    Lead = "Lead"


class PositionEnum(str, enum.Enum):
    Frontend = "Frontend Developer"
    Backend = "Backend Developer"
    Fullstack = "Fullstack Developer"
    Designer = "Designer"
    QA = "QA Engineer"
    PM = "Project Manager"


class Employee(IdIntPkMixin, Person):
    salary: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    grade: Mapped[GradeEnum] = mapped_column(Enum(GradeEnum), nullable=False)
    position: Mapped[PositionEnum] = mapped_column(Enum(PositionEnum), nullable=False)

    teams: Mapped[list["EmployeeTeam"]] = relationship("EmployeeTeam", back_populates="employee")

    __table_args__ = (
        CheckConstraint("salary >= 0", name="ck_employee_salary_positive"),
    )

    @validates("salary")
    def validate_salary(self, key: str, value: Decimal) -> Decimal: # noqa: F841
        if value < 0:
            raise ValueError("Salary must be positive")
        return value


class Team(IdIntPkMixin, Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"))
    teamlead_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id", ondelete="SET NULL"))

    members: Mapped[list["EmployeeTeam"]] = relationship("EmployeeTeam", back_populates="team")


class EmployeeTeam(IdIntPkMixin, Base):
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)

    employee: Mapped["Employee"] = relationship("Employee", back_populates="teams")
    team: Mapped["Team"] = relationship("Team", back_populates="members")

    __table_args__ = (
        UniqueConstraint("employee_id", "team_id", name="uq_employee_team"),
    )
