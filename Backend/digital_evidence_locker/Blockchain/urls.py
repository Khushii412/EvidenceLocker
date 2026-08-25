from django.urls import path
from . import views


app_name = "blockchain"

urlpatterns = [
    path(
        "",
        views.blockchain_transactions,
        name="blockchain_transactions"
    ),
]