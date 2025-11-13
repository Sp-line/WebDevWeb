from pydantic import BaseModel, Field, ConfigDict

from schemas.common import ProjectShort, PersonShort


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


class EmployeeTeamMember(BaseModel):
    id: int
    employee: PersonShort

    model_config = ConfigDict(from_attributes=True)


class TeamResponseBase(BaseModel):
    id: int
    name: str
    project: ProjectShort | None
    teamlead: PersonShort | None


class TeamResponse(TeamResponseBase):
    pass


class TeamListResponse(BaseModel):
    teams: list[TeamResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)


class TeamDetailResponse(TeamResponseBase):
    members: list[EmployeeTeamMember] = []

    model_config = ConfigDict(from_attributes=True)
