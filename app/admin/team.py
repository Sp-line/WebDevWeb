from sqladmin import ModelView

from app.admin.core import register_admin
from app.models import Team


@register_admin
class TeamAdmin(ModelView, model=Team):
    column_list = [
        Team.id,
        Team.name,
        Team.project_id,
        Team.teamlead_id
    ]
