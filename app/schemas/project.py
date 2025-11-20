from datetime import datetime

from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationInfo

from app.constants.project import NAME_MAX_LEN, NAME_MIN_LEN
from app.schemas.common import OrderShort, TeamShort
from app.utils.utc_now import utc_now


class ProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=NAME_MIN_LEN,
        max_length=NAME_MAX_LEN,
    )
    description: str | None = Field(None)
    start_date: datetime = Field(default_factory=utc_now)
    end_date: datetime | None = Field(None)

    @field_validator("end_date")
    def end_date_after_start_date(cls, v: datetime | None, info: ValidationInfo) -> datetime | None:
        start: datetime | None = info.data.get("start_date")
        if v is not None and start is not None and v < start:
            raise ValueError("end_date must be after start_date")
        return v


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    name: str | None = Field(
        None,
        min_length=NAME_MIN_LEN,
        max_length=NAME_MAX_LEN,
    )


class ProjectResponseBase(BaseModel):
    id: int
    name: str
    start_date: datetime | None
    end_date: datetime | None


class ProjectListResponse(ProjectResponseBase):
    model_config = ConfigDict(from_attributes=True)


class ProjectResponse(ProjectResponseBase):
    description: str | None
    order: OrderShort | None
    teams: list[TeamShort] = []

    model_config = ConfigDict(from_attributes=True)
