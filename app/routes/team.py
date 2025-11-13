from typing import Annotated

from fastapi import APIRouter, Depends, status

from dependencies.team import get_team_service
from schemas.team import (
    TeamCreate,
    TeamUpdate,
    TeamListResponse,
    TeamDetailResponse,
    TeamCreateUpdateResponse,
)
from services.team import TeamService

team_router = APIRouter(prefix="/teams", tags=["Teams"])


@team_router.get("/", response_model=TeamListResponse)
async def list_teams(service: Annotated[TeamService, Depends(get_team_service)]) -> TeamListResponse:
    return await service.get_all_with_project_and_teamlead()


@team_router.get("/{team_id}", response_model=TeamDetailResponse)
async def retrieve_team(team_id: int, service: Annotated[TeamService, Depends(get_team_service)]) -> TeamDetailResponse:
    return await service.get_with_project_teamlead_and_members(team_id)


@team_router.post("/", response_model=TeamCreateUpdateResponse, status_code=status.HTTP_201_CREATED)
async def create_team(data: TeamCreate,
                      service: Annotated[TeamService, Depends(get_team_service)]) -> TeamCreateUpdateResponse:
    return await service.create(data)


@team_router.patch("/{team_id}", response_model=TeamCreateUpdateResponse)
async def update_team(team_id: int, data: TeamUpdate,
                      service: Annotated[TeamService, Depends(get_team_service)]) -> TeamCreateUpdateResponse:
    return await service.update(team_id, data)


@team_router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: int, service: Annotated[TeamService, Depends(get_team_service)]) -> None:
    await service.delete(team_id)
