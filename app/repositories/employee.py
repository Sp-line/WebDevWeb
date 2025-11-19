from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Employee
from app.repositories.base import RepositoryBase
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeRepository(RepositoryBase[Employee, EmployeeCreate, EmployeeUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Employee, session)
