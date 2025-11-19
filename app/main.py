from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.admin.core import init_admin
from app.config import settings
from app.database import database
from app.routes import router as api_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    yield
    await database.dispose()


main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

init_admin(main_app, database.engine)

main_app.include_router(
    api_router,
    prefix=settings.api.prefix,
)

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
