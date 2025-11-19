from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.team import TeamService
from database import database as db


async def get_team_service(session: Annotated[AsyncSession, Depends(db.get_session)]) -> TeamService:
    return TeamService(session)
