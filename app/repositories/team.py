from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Team, EmployeeTeam
from repositories.base import RepositoryBase
from schemas.team import TeamCreate, TeamUpdate


class TeamRepository(RepositoryBase[Team, TeamCreate, TeamUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Team, session)

    async def get_all_with_project_and_teamlead(self) -> Sequence[Team]:
        stmt = select(Team).options(
            selectinload(Team.project),
            selectinload(Team.teamlead),
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_with_project_teamlead_and_members(self, team_id: int) -> Team | None:
        stmt = (
            select(Team)
            .where(Team.id == team_id)
            .options(
                selectinload(Team.project),
                selectinload(Team.teamlead),
                selectinload(Team.members).selectinload(EmployeeTeam.employee),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_team_by_teamlead_id(self, teamlead_id: int) -> Team | None:
        stmt = select(Team).where(Team.teamlead_id == teamlead_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()