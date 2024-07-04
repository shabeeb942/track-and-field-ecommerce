from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from . import tables
from .models import User
from core import mixins
from registration.backends.default.views import RegistrationView
from .forms import CustomRegistrationForm

class CustomRegistrationView(RegistrationView):
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('web:index')

    def register(self, form):
        user = form.save(commit=False)
        user.save()

        # Authenticate and login the user
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)

        return user

class UserListView(mixins.HybridListView):
    model = User
    table_class = tables.UserTable
    filterset_fields = ("is_active", "is_staff")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(kwargs)
        context["title"] = "Users"
        context["can_add"] = True
        context["new_link"] = reverse_lazy("accounts:user_create")
        return context

class UserDetailView(mixins.HybridDetailView):
    model = User

class UserCreateView(mixins.HybridCreateView):
    model = User
    exclude = ("is_active", "date_joined", "user_permissions", "groups", "last_login", "is_superuser", "is_staff")

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data["password"])
        return super().form_valid(form)

class UserUpdateView(mixins.HybridUpdateView):
    model = User
    exclude = (
        "is_active",
        "password",
        "date_joined",
        "user_permissions",
        "groups",
        "last_login",
        "is_superuser",
        "is_staff",
    )

class UserDeleteView(mixins.HybridDeleteView):
    model = User
