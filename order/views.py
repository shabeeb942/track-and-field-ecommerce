from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Order
from . import tables
from core import mixins
# Create your views here.

class OrderListView(mixins.HybridListView):
    model = Order
    table_class = tables.OrderTables
    filterset_fields = ("order_id",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Order"
        context["can_add"] = True
        context["new_link"] = reverse_lazy("web:banner_create")
        return context

from django.shortcuts import get_object_or_404

class OrderDetailView(mixins.HybridDetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        order_items = order.orderitem_set.all()
        context["order_items"] = order_items
        return context

class OrderUpdateView(mixins.HybridUpdateView):
    model = Order
    fields = ("","sub_category")

class OrderDeleteView(mixins.HybridDeleteView):
    model = Order
