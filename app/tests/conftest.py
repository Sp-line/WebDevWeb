import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio

os.environ.setdefault("APP_CONFIG__DB__URL", "postgresql+asyncpg://test:test@localhost:5432/test_db")

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from app.database import database as db
from app.models import Base

from app.main import main_app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=engine_test,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_session():
        yield db_session

    app = main_app

    app.dependency_overrides[db.get_session] = override_get_session # type: ignore

    async with AsyncClient(transport=ASGITransport(app=main_app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear() # type: ignore
