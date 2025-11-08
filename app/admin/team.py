from sqladmin import ModelView

from admin.core import register_admin
from models import Team


@register_admin
class TeamAdmin(ModelView, model=Team):
    column_list = [
        Team.id,
        Team.name,
        Team.project_id,
        Team.teamlead_id
    ]
