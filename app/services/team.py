from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from repositories.employee import EmployeeRepository
from repositories.project import ProjectRepository
from repositories.team import TeamRepository
from schemas.team import TeamListResponse, TeamCreate, TeamUpdate, TeamDetailResponse, \
    TeamCreateUpdateResponse
from utils.get_obj_or_404 import get_object_or_404

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class TeamService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TeamRepository(session)
        self.project_repo = ProjectRepository(session)
        self.employee_repo = EmployeeRepository(session)

    async def get_all_with_project_and_teamlead(self) -> TeamListResponse:
        teams = await self.repo.get_all_with_project_and_teamlead()
        return TeamListResponse.model_validate(
            {
                "teams": teams,
                "total": len(teams)
            },
            from_attributes=True
        )

    async def get_with_project_teamlead_and_members(self, team_id: int) -> TeamDetailResponse:
        team = await self.repo.get_with_project_teamlead_and_members(team_id)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Team with id={team_id} not found'
            )
        return TeamDetailResponse.model_validate(team)

    async def create(self, data: TeamCreate) -> TeamCreateUpdateResponse:
        if data.project_id:
            await get_object_or_404(self.session ,self.project_repo.model, data.project_id)

        if data.teamlead_id:
            await get_object_or_404(self.session, self.employee_repo.model, data.teamlead_id)

            existing_team = await self.repo.get_team_by_teamlead_id(data.teamlead_id)
            if existing_team:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Employee id={data.teamlead_id} is already a teamlead for team id={existing_team.id}"
                )

        team = await self.repo.create(data)
        return TeamCreateUpdateResponse.model_validate(team)

    async def update(self, team_id: int, data: TeamUpdate) -> TeamCreateUpdateResponse:
        team = await self.repo.update(team_id, data)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Team with id={team_id} not found'
            )
        return TeamCreateUpdateResponse.model_validate(team)

    async def delete(self, team_id: int) -> None:
        deleted = await self.repo.delete(team_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Team with id={team_id} not found"
            )
        return None
