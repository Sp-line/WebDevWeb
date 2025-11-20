from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from app.models import Team
from app.schemas.team import TeamCreate
from app.services.team import TeamService

pytestmark = pytest.mark.asyncio


async def test_create_team_success(mocker):
    mock_session = AsyncMock()
    service = TeamService(mock_session)

    mocker.patch.object(service.project_repo, 'get_by_id', return_value=True)
    mocker.patch.object(service.employee_repo, 'get_by_id', return_value=True)
    mocker.patch.object(service.repo, 'get_team_by_teamlead_id', return_value=None)

    expected_team = Team(id=1, name="Alpha Squad", project_id=1, teamlead_id=5)
    mocker.patch.object(service.repo, 'create', return_value=expected_team)

    data = TeamCreate(name="Alpha Squad", project_id=1, teamlead_id=5)

    result = await service.create(data)

    assert result.id == 1
    assert result.name == "Alpha Squad"

    service.repo.create.assert_awaited_once()


async def test_create_team_fail_duplicate_teamlead(mocker):
    mock_session = AsyncMock()
    service = TeamService(mock_session)

    mocker.patch.object(service.project_repo, 'get_by_id', return_value=True)
    mocker.patch.object(service.employee_repo, 'get_by_id', return_value=True)

    existing_team = Team(id=2, name="Beta", teamlead_id=5)
    mocker.patch.object(service.repo, 'get_team_by_teamlead_id', return_value=existing_team)

    data = TeamCreate(name="Alpha Squad", project_id=1, teamlead_id=5)

    with pytest.raises(HTTPException) as exc:
        await service.create(data)

    assert exc.value.status_code == 400
    assert "already a teamlead" in exc.value.detail
