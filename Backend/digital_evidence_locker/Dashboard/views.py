
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Cases.models import Case
from Evidence.models import Evidence
from Accounts.models import User
from Audit.models import AuditLog


@login_required
def dashboard(request):
    user = request.user

    # Get cases visible to the current user.
    cases = Case.objects.all()

    if user.role == User.Role.INVESTIGATOR:
        cases = cases.filter(assigned_investigator=user)

    elif user.role == User.Role.FORENSIC_EXPERT:
        cases = cases.filter(assigned_forensic_expert=user)

    elif user.role == User.Role.JUDGE:
        cases = cases.filter(assigned_judge=user)

    # Get evidence belonging to visible cases.
    evidence = Evidence.objects.filter(case__in=cases)

    # Admin sees all recent activity.
    # Other roles see activity related to their assigned cases.
    if user.role == User.Role.ADMIN:
        recent_activities = AuditLog.objects.select_related(
            "user"
        ).order_by("-timestamp")[:10]
    else:
        recent_activities = AuditLog.objects.filter(
            case_id__in=cases.values("id")
        ).select_related("user").order_by("-timestamp")[:10]

    context = {
        "open_cases_count": cases.filter(
            status=Case.Status.OPEN
        ).count(),

        "closed_cases_count": cases.filter(
            status=Case.Status.CLOSED
        ).count(),

        "evidence_count": evidence.count(),

        "pending_users_count": (
            User.objects.filter(
                is_approved=False,
                is_active=True
            ).exclude(role=User.Role.ADMIN).count()
            if user.role == User.Role.ADMIN else 0
        ),

        "recent_activities": recent_activities,
        "dashboard_cases": cases.order_by("-updated_at")[:5],
    }

    # Admin and non-admin dashboards use different templates.
    if user.role == User.Role.ADMIN:
        template_name = "admin/dashboard.html"
    else:
        template_name = "accounts/user_dashboard.html"

    return render(request, template_name, context)
