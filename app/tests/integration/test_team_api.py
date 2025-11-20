from decimal import Decimal

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Project, Employee, Team
from app.constants.employee import GradeEnum, PositionEnum

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def project_fix(db_session: AsyncSession):
    p = Project(name="API Project")
    db_session.add(p)
    await db_session.commit()
    await db_session.refresh(p)
    return p


@pytest_asyncio.fixture
async def employee_fix(db_session: AsyncSession):
    e = Employee(first_name="Test", last_name="User", email="api@test.com", salary=Decimal(1000), grade=GradeEnum.Middle,
                 position=PositionEnum.Backend)
    db_session.add(e)
    await db_session.commit()
    await db_session.refresh(e)
    return e


async def test_api_create_team(async_client: AsyncClient, project_fix, employee_fix):
    payload = {
        "name": "Dream Team",
        "project_id": project_fix.id,
        "teamlead_id": employee_fix.id
    }
    response = await async_client.post("/api/teams/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Dream Team"
    assert data["project_id"] == project_fix.id


async def test_api_get_list(async_client: AsyncClient, db_session: AsyncSession, project_fix):
    t1 = Team(name="A-Team", project_id=project_fix.id)
    t2 = Team(name="B-Team", project_id=project_fix.id)
    db_session.add_all([t1, t2])
    await db_session.commit()

    response = await async_client.get("/api/teams/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["teams"]) == 2
    assert data["teams"][0]["project"]["name"] == "API Project"


@pytest.mark.parametrize("payload, expected_status, error_msg", [
    ({"project_id": 1}, 422, "Field required"),
    ({"name": "Valid", "project_id": 9999}, 404, "Project with id=9999 not found"),
])
async def test_api_create_validation_errors(
        async_client: AsyncClient,
        payload,
        expected_status,
        error_msg
):
    response = await async_client.post("/api/teams/", json=payload)
    assert response.status_code == expected_status
    if expected_status == 404:
        assert error_msg in response.json()["detail"]


async def test_api_assign_busy_teamlead(async_client: AsyncClient, project_fix, employee_fix, db_session: AsyncSession):
    t1 = Team(name="Existing", teamlead_id=employee_fix.id, project_id=project_fix.id)
    db_session.add(t1)
    await db_session.commit()

    payload = {
        "name": "New Team",
        "project_id": project_fix.id,
        "teamlead_id": employee_fix.id
    }
    response = await async_client.post("/api/teams/", json=payload)

    assert response.status_code == 400
    assert "already a teamlead" in response.json()["detail"]


async def test_api_update_team(async_client: AsyncClient, db_session: AsyncSession):
    team = Team(name="Old Name")
    db_session.add(team)
    await db_session.commit()

    payload = {"name": "New Name"}
    response = await async_client.patch(f"/api/teams/{team.id}", json=payload)

    assert response.status_code == 200
    assert response.json()["name"] == "New Name"

    await db_session.refresh(team)
    assert team.name == "New Name"


async def test_api_delete_team(async_client: AsyncClient, db_session: AsyncSession):
    team = Team(name="To Delete")
    db_session.add(team)
    await db_session.commit()

    response = await async_client.delete(f"/api/teams/{team.id}")
    assert response.status_code == 204

    response_get = await async_client.get(f"/api/teams/{team.id}")
    assert response_get.status_code == 404