from decimal import Decimal

from pydantic import BaseModel, Field

from app.constants.order import TECHNICAL_TASK_MAX_LEN


class OrderBase(BaseModel):
    client_id: int = Field(...)
    project_id: int = Field(...)
    price: Decimal = Field(..., gt=0)
    technical_task: str | None = Field(
        None,
        max_length=TECHNICAL_TASK_MAX_LEN,
    )


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    client_id: int | None = Field(None)
    project_id: int | None = Field(None)
    price: Decimal | None = Field(None, gt=0)
