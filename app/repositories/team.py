from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Team, EmployeeTeam
from repositories.base import RepositoryBase
from schemas.team import TeamCreate, TeamUpdate


class TeamRepository(RepositoryBase[Team, TeamCreate, TeamUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Team, session)

    async def get_with_members(self, team_id: int) -> Team | None:
        stmt = select(Team).where(Team.id == team_id).options(
            selectinload(Team.members).selectinload(EmployeeTeam.employee)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()