from __future__ import annotations

from typing import TYPE_CHECKING

from sqladmin import ModelView

from app.admin.core import register_admin
from app.models import Client
from app.schemas.person import PersonBase

if TYPE_CHECKING:
    from typing import Any
    from fastapi import Request


@register_admin
class ClientAdmin(ModelView, model=Client):
    column_list = [
        Client.id,
        Client.first_name,
        Client.last_name,
        Client.email
    ]

    async def on_model_change(self, data: dict[str, Any], model: Any, is_created: bool, request: Request) -> None:
        PersonBase(**data)
