from sqlalchemy.ext.asyncio import AsyncSession

from models import Employee
from repositories.base import RepositoryBase
from schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeRepository(RepositoryBase[Employee, EmployeeCreate, EmployeeUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Employee, session)