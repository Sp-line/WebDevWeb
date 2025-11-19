from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr, ConfigDict


class PersonShort(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class ProjectShort(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class TeamShort(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class OrderShort(BaseModel):
    id: int
    price: Decimal
    created: datetime

    model_config = ConfigDict(from_attributes=True)
