from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Project
from app.repositories.base import RepositoryBase
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository(RepositoryBase[Project, ProjectCreate, ProjectUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Project, session)

    async def get_with_order_and_teams(self, project_id: int) -> Project | None:
        stmt = select(Project).where(Project.id == project_id).options(
            selectinload(Project.order),
            selectinload(Project.teams)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
