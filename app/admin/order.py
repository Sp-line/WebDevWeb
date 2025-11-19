from sqladmin import ModelView

from app.admin.core import register_admin
from app.models import Order


@register_admin
class OrderAdmin(ModelView, model=Order):
    column_list = [
        Order.id,
        Order.client_id,
        Order.project_id,
        Order.price,
        Order.technical_task,
        Order.created,
    ]
