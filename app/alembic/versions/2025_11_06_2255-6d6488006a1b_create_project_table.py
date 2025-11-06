"""create project table

Revision ID: 6d6488006a1b
Revises:
Create Date: 2025-11-06 22:55:05.779959

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "6d6488006a1b"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "start_date",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("end_date", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            "start_date IS NULL OR end_date IS NULL OR end_date >= start_date",
            name=op.f("ck_projects_ck_project_dates"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_projects")),
    )


def downgrade() -> None:
    op.drop_table("projects")
