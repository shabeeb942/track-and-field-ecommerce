from core.base import BaseTable
from .models import Order
from .models import OrderItem

class OrderTables(BaseTable):
    class Meta:
        model = Order
        fields = ("order_id","full_name")
        attrs = {"class": "table key-buttons border-bottom"}


class OrderItemTables(BaseTable):
    class Meta:
        model = OrderItem
        fields = ("order_item_id","product","quantity")
        attrs = {"class": "table key-buttons border-bottom"}
