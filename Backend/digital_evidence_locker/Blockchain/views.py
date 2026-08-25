from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import BlockchainTransaction


@login_required
def blockchain_transactions(request):
    transactions = BlockchainTransaction.objects.all().order_by("-timestamp")

    return render(
        request,
        "blockchain/transactions.html",
        {"transactions": transactions}
    )