from sqladmin import ModelView

from admin.core import register_admin
from models import Employee


@register_admin
class EmployeeAdmin(ModelView, model=Employee):
    column_list = [
        Employee.id,
        Employee.first_name,
        Employee.last_name,
        Employee.position,
        Employee.grade,
        Employee.salary,
        Employee.joined,
    ]