from django.urls import path

from . import views
from .views import login_view


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard",
    ),
    path(
        "user-dashboard/",
        views.user_dashboard,
        name="user_dashboard",
    ),
]