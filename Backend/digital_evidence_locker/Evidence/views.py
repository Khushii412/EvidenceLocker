from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EvidenceForm
from .models import Evidence, EvidenceActivity
from Blockchain.services import store_evidence_hash


@login_required
def evidence_list(request):

    evidence = Evidence.objects.select_related(
        "case",
        "uploaded_by"
    )

    return render(
        request,
        "evidence/evidence_list.html",
        {
            "evidence": evidence
        }
    )


@login_required
def evidence_detail(request, evidence_id):

    evidence = get_object_or_404(
        Evidence.objects.select_related(
            "case",
            "uploaded_by"
        ),
        id=evidence_id
    )

    activities = evidence.activities.select_related(
        "user"
    )

    EvidenceActivity.objects.create(
        evidence=evidence,
        user=request.user,
        action=EvidenceActivity.Action.VIEWED,
        description="Evidence viewed."
    )

    return render(
        request,
        "evidence/evidence_detail.html",
        {
            "evidence": evidence,
            "activities": activities
        }
    )


@login_required
def upload_evidence(request):

    if request.method == "POST":

        form = EvidenceForm(request.POST, request.FILES)

        if form.is_valid():

            evidence = form.save(commit=False)
            evidence.uploaded_by = request.user
            evidence.save()

            # Store evidence hash on blockchain
            blockchain_result = store_evidence_hash(evidence.file_hash)

            if blockchain_result["success"]:
                evidence.blockchain_tx_hash = blockchain_result["transaction_hash"]
                evidence.blockchain_block_number = blockchain_result["block_number"]
                evidence.save(update_fields=["blockchain_tx_hash", "blockchain_block_number"])

            messages.success(
                request,
                "Evidence uploaded successfully."
            )

            return redirect(
                "evidence:evidence_detail",
                evidence_id=evidence.id
            )

    else:
        form = EvidenceForm()

    return render(
        request,
        "evidence/evidence_form.html",
        {
            "form": form,
            "page_title": "Upload Evidence"
        }
    )