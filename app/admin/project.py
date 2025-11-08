from __future__ import annotations

from typing import TYPE_CHECKING

from sqladmin import ModelView

from admin.core import register_admin
from models import Project
from schemas.project import ProjectBase

if TYPE_CHECKING:
    from typing import Any
    from fastapi import Request


@register_admin
class ProjectAdmin(ModelView, model=Project):
    column_list = [
        Project.id,
        Project.name,
        Project.start_date,
        Project.end_date,
    ]

    async def on_model_change(self, data: dict[str, Any], model: Any, is_created: bool, request: Request) -> None:
        ProjectBase(**data)
