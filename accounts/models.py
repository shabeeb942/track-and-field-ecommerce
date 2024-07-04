from django.contrib.auth.models import AbstractUser
from django.db import models
from core.functions import generate_fields
from django.urls import reverse_lazy

class User(AbstractUser):
    # Removed usertype and shop_name fields

    def get_fields(self):
        return generate_fields(self)

    def get_absolute_url(self):
        return reverse_lazy("accounts:user_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("accounts:user_list")

    def get_update_url(self):
        return reverse_lazy("accounts:user_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("accounts:user_delete", kwargs={"pk": self.pk})

    @property
    def fullname(self):
        return self.username

    def __str__(self):
        return self.username
