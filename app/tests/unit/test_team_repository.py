from decimal import Decimal

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.team import TeamRepository
from app.models import Team, Project, Employee, EmployeeTeam
from app.constants.employee import GradeEnum, PositionEnum

from app.schemas.team import TeamCreate, TeamDetailResponse

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def setup_data(db_session: AsyncSession):
    proj = Project(name="Manhattan", description="Big Bomb")
    db_session.add(proj)

    lead = Employee(first_name="Oppen", last_name="Heimer", email="oppen@test.com", salary=Decimal(100),
                    grade=GradeEnum.Senior,
                    position=PositionEnum.PM)
    dev = Employee(first_name="Richard", last_name="Feynman", email="richard@test.com", salary=Decimal(100),
                   grade=GradeEnum.Junior, position=PositionEnum.Backend)
    db_session.add_all([lead, dev])
    await db_session.commit()
    await db_session.refresh(proj)
    await db_session.refresh(lead)
    await db_session.refresh(dev)
    return {"project": proj, "lead": lead, "dev": dev}


async def test_repo_create_and_get_full_info(db_session: AsyncSession, setup_data):
    repo = TeamRepository(db_session)
    project = setup_data["project"]
    lead = setup_data["lead"]

    schema = TeamCreate(name="Physics", project_id=project.id, teamlead_id=lead.id)
    team = await repo.create(schema)
    assert team.id is not None

    fetched_team_orm = await repo.get_with_project_teamlead_and_members(team.id)

    response_model = TeamDetailResponse.model_validate(fetched_team_orm)

    assert response_model.name == "Physics"
    assert response_model.project.name == "Manhattan"
    assert response_model.teamlead.last_name == "Heimer"
    assert response_model.teamlead.id == lead.id


async def test_repo_members_loading(db_session: AsyncSession, setup_data):
    repo = TeamRepository(db_session)

    team = Team(name="Devs", project_id=setup_data["project"].id)
    db_session.add(team)
    await db_session.commit()

    member_link = EmployeeTeam(employee_id=setup_data["dev"].id, team_id=team.id)
    db_session.add(member_link)
    await db_session.commit()

    fetched_team_orm = await repo.get_with_project_teamlead_and_members(team.id)

    response_model = TeamDetailResponse.model_validate(fetched_team_orm)

    assert len(response_model.members) == 1

    assert response_model.members[0].employee.last_name == "Feynman"
    assert response_model.members[0].employee.email == "richard@test.com"