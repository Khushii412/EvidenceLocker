from django.urls import path
from . import views


app_name = "Cases"


urlpatterns = [
    path("", views.case_list, name="case_list"),

    path(
        "create/",
        views.create_case,
        name="create_case"
    ),

    path(
        "<int:case_id>/",
        views.case_detail,
        name="case_detail"
    ),

    path(
        "<int:case_id>/edit/",
        views.edit_case,
        name="edit_case"
    ),

    path(
        "<int:case_id>/delete/",
        views.delete_case,
        name="delete_case"
    ),
]