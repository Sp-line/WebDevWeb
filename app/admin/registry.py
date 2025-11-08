from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqladmin import ModelView
    from typing import Type, Callable


def create_admin_registry() -> tuple[Callable, Callable]:
    registry: list[Type[ModelView]] = []

    def register_admin(cls: Type[ModelView]) -> Type[ModelView]:
        registry.append(cls)
        return cls

    def get_registered() -> list[Type[ModelView]]:
        return list(registry)

    return register_admin, get_registered
