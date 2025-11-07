from pydantic import BaseModel, Field


class TeamBase(BaseModel):
    name: str = Field(
        ...,
    )
    project_id: int | None = Field(None)
    teamlead_id: int | None = Field(None)


class TeamCreate(TeamBase):
    pass


class TeamUpdate(TeamBase):
    name: str | None = Field(None)