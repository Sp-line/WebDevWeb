from typing import Type, TypeVar

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


async def get_object_or_404(session: AsyncSession, model: Type[ModelType], obj_id: int) -> ModelType:
    obj = await session.get(model, obj_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} with id={obj_id} not found"
        )
    return obj
