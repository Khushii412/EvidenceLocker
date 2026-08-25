from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import AuditLog


@login_required
def audit_log_list(request):

    logs = AuditLog.objects.select_related("user").all()

    return render(
        request,
        "audit/audit_log_list.html",
        {"logs": logs}
    )