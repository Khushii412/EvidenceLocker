from django.urls import path
from . import views


urlpatterns = [

    path("login/", views.login_view, name="login"),

    path("logout/", views.logout_view, name="logout"),

    path("register/", views.register_view, name="register"),

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