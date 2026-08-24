from django.urls import path

from . import views


app_name = "evidence"


urlpatterns = [

    path(
        "",
        views.evidence_list,
        name="evidence_list"
    ),

    path(
        "upload/",
        views.upload_evidence,
        name="upload_evidence"
    ),

    path(
        "<int:evidence_id>/",
        views.evidence_detail,
        name="evidence_detail"
    ),
]