"""create employee team and employeeteam tables

Revision ID: b1e28ceec15c
Revises: 44f5416aeebf
Create Date: 2025-11-06 23:08:42.918921

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b1e28ceec15c"
down_revision: Union[str, Sequence[str], None] = "44f5416aeebf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("salary", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column(
            "joined",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "grade",
            sa.Enum("Junior", "Middle", "Senior", "Lead", name="gradeenum"),
            nullable=False,
        ),
        sa.Column(
            "position",
            sa.Enum(
                "Frontend",
                "Backend",
                "Fullstack",
                "Designer",
                "QA",
                "PM",
                name="positionenum",
            ),
            nullable=False,
        ),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.CheckConstraint(
            "salary >= 0",
            name=op.f("ck_employees_ck_employee_salary_positive"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_employees")),
        sa.UniqueConstraint("email", name=op.f("uq_employees_email")),
    )
    op.create_table(
        "teams",
        sa.PrimaryKeyConstraint("id", name=op.f("pk_teams")),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column("teamlead_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_teams_project_id_projects"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["teamlead_id"],
            ["employees.id"],
            name=op.f("fk_teams_teamlead_id_employees"),
            ondelete="SET NULL",
        ),
    )
    op.create_table(
        "employee_teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["employee_id"],
            ["employees.id"],
            name=op.f("fk_employee_teams_employee_id_employees"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
            name=op.f("fk_employee_teams_team_id_teams"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_employee_teams")),
        sa.UniqueConstraint("employee_id", "team_id", name="uq_employee_team"),
    )


def downgrade() -> None:
    op.drop_table("employee_teams")
    op.drop_table("teams")
    op.drop_table("employees")
