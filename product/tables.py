from core.base import BaseTable

from .models import Category,SubCategory,Product
from django_tables2 import columns
import django_tables2 as tables


class CategoryTable(BaseTable):
    class Meta:
        model = Category
        fields = ("name",)
        attrs = {"class": "table key-buttons border-bottom"}


class SubCategoryTable(BaseTable):
    class Meta:
        model = SubCategory
        fields = ("name",)
        attrs = {"class": "table key-buttons border-bottom"}
        

class ProductTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <a href="{{ record.get_absolute_dashboard_url }}" class="btn btn-sm btn-light btn-outline-info">OPEN</a>

        """,
        orderable=False,
    )
    class Meta:
        model = Product
        fields = ("name",)
        attrs = {"class": "table key-buttons border-bottom"}