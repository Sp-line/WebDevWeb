from fastapi import APIRouter

from app.routes.team import team_router

router = APIRouter()

router.include_router(team_router)
