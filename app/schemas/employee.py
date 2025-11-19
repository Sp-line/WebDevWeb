from datetime import datetime
from decimal import Decimal

from pydantic import Field, BaseModel, ConfigDict, EmailStr

from app.constants.employee import GradeEnum, PositionEnum
from app.constants.person import EMAIL_MAX_LEN, FIRST_NAME_MIN_LEN, FIRST_NAME_MAX_LEN, LAST_NAME_MIN_LEN, \
    LAST_NAME_MAX_LEN
from app.schemas.person import PersonBase


class EmployeeBase(PersonBase):
    salary: Decimal = Field(..., gt=0)
    grade: GradeEnum
    position: PositionEnum


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    first_name: str | None = Field(None, min_length=FIRST_NAME_MIN_LEN, max_length=FIRST_NAME_MAX_LEN)
    last_name: str | None = Field(None, min_length=LAST_NAME_MIN_LEN, max_length=LAST_NAME_MAX_LEN)
    email: EmailStr | None = Field(None, max_length=EMAIL_MAX_LEN)
    salary: Decimal | None = Field(None, gt=0)
    grade: GradeEnum | None = None
    position: PositionEnum | None = None


class EmployeeResponse(EmployeeBase):
    id: int
    joined: datetime

    model_config = ConfigDict(from_attributes=True)
