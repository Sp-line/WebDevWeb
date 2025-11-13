from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import database as db
from services.team import TeamService


async def get_team_service(session: Annotated[AsyncSession, Depends(db.get_session)]) -> TeamService:
    return TeamService(session)
