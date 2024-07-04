from core.base import BaseTable
from django_tables2 import columns

from .models import User


class UserTable(BaseTable):
    username = columns.Column(linkify=True)
    date_joined = columns.DateTimeColumn(format="d/m/y")
    created = None

    class Meta:
        model = User
        fields = ("username", "date_joined", "last_login", "is_active", "is_staff", "is_superuser")
        attrs = {"class": "table key-buttons border-bottom"}
