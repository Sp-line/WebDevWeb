from __future__ import annotations

from typing import TYPE_CHECKING

from sqladmin import Admin

from admin.registry import create_admin_registry

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine
    from fastapi import FastAPI

register_admin, get_registered_admins = create_admin_registry()


def init_admin(app: FastAPI, engine: AsyncEngine) -> Admin:
    admin = Admin(app, engine)

    for view_class in get_registered_admins():
        admin.add_view(view_class)

    return admin
