from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Report


@login_required
def report_list(request):

    reports = Report.objects.select_related("created_by").all()

    return render(
        request,
        "reports/report_list.html",
        {"reports": reports}
    )


@login_required
def report_detail(request, report_id):

    report = Report.objects.get(id=report_id)

    return render(
        request,
        "reports/report_detail.html",
        {"report": report}
    )