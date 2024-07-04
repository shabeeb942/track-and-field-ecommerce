from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import CustomRegistrationView

app_name = "accounts"

urlpatterns = [
    path('user/register/', CustomRegistrationView.as_view(), name='registration_register'),
    
    path("", views.UserListView.as_view(), name="user_list"),
    path("user/<str:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("new/user/", views.UserCreateView.as_view(), name="user_create"),
    path("user/<str:pk>/update/", views.UserUpdateView.as_view(), name="user_update"),
    path("user/<str:pk>/delete/", views.UserDeleteView.as_view(), name="user_delete"),
]