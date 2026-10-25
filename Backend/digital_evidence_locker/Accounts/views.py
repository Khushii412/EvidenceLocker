from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
#from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm

from .models import User


def login_view(request):
    """
    Handles user login.
    Only approved and active users can log in.
    """

    if request.user.is_authenticated:
        if request.user.role == User.Role.ADMIN:
            return redirect("admin_dashboard")
        return redirect("user_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if not user.is_active:
                messages.error(
                    request,
                    "Your account has been deactivated."
                )
                return redirect("login")

            if not user.is_approved:
                messages.warning(
                    request,
                    "Your account is waiting for Admin approval."
                )
                return redirect("login")

            login(request, user)

            if user.role == User.Role.ADMIN:
                return redirect("admin_dashboard")

            return redirect("user_dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    """
    Logs the current user out.
    """

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")



@login_required
def admin_dashboard(request):
    """
    Admin dashboard with case, evidence, user, and activity statistics.
    """

    if request.user.role != User.Role.ADMIN:
        messages.error(
            request,
            "You are not authorized to access the Admin Dashboard."
        )
        return redirect("user_dashboard")

    from Cases.models import Case
    from Evidence.models import Evidence
    from Audit.models import AuditLog

    cases = Case.objects.all()
    evidence = Evidence.objects.all()

    context = {
        # Existing user statistics
        "total_users": User.objects.count(),
        "approved_users": User.objects.filter(
            is_approved=True
        ).count(),
        "pending_users": User.objects.filter(
            is_approved=False,
            is_active=True
        ).exclude(role=User.Role.ADMIN).count(),
        "active_users": User.objects.filter(
            is_active=True
        ).count(),

        # Case and evidence statistics
        "open_cases_count": cases.filter(
            status=Case.Status.OPEN
        ).count(),
        "closed_cases_count": cases.filter(
            status=Case.Status.CLOSED
        ).count(),
        "evidence_count": evidence.count(),

        # Recent cases
        "dashboard_cases": cases.order_by("-updated_at")[:5],

        # Recent system activities
        "recent_activities": AuditLog.objects.select_related(
            "user"
        ).order_by("-timestamp")[:10],
    }

    return render(
        request,
        "admin/dashboard.html",
        context
    )



@login_required
def user_dashboard(request):
    from Cases.models import Case
    from Evidence.models import Evidence
    from Audit.models import AuditLog

    user = request.user

    # Show only cases assigned to this user.
    cases = Case.objects.none()

    if user.role == User.Role.INVESTIGATOR:
        cases = Case.objects.filter(assigned_investigator=user)

    elif user.role == User.Role.FORENSIC_EXPERT:
        cases = Case.objects.filter(assigned_forensic_expert=user)

    elif user.role == User.Role.JUDGE:
        cases = Case.objects.filter(assigned_judge=user)

    # Evidence related to assigned cases.
    evidence = Evidence.objects.filter(case__in=cases)

    # Recent activity related to assigned cases.
    recent_activities = AuditLog.objects.filter(
        case_id__in=cases.values("id")
    ).select_related("user").order_by("-timestamp")[:5]

    context = {
        "dashboard_cases": cases.order_by("-updated_at")[:5],

        "total_cases_count": cases.count(),

        "open_cases_count": cases.filter(
            status=Case.Status.OPEN
        ).count(),

        "closed_cases_count": cases.filter(
            status=Case.Status.CLOSED
        ).count(),

        "evidence_count": evidence.count(),

        "forensic_pending_count": cases.filter(
            status=Case.Status.UNDER_INVESTIGATION
        ).count() if user.role == User.Role.FORENSIC_EXPERT else 0,

        "court_cases_count": cases.filter(
            status=Case.Status.SUBMITTED_TO_COURT
        ).count() if user.role == User.Role.JUDGE else 0,

        "recent_activities": recent_activities,
    }

    return render(
        request,
        "accounts/user_dashboard.html",
        context
    )



def register_view(request):

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Account created successfully. Please log in."
            )

            return redirect("login")

    else:
        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )



@login_required
def user_management(request):
    if request.user.role != User.Role.ADMIN:
        messages.error(
            request,
            "You are not authorized to manage users."
        )
        return redirect("user_dashboard")

    users = User.objects.all().order_by("username")

    return render(
        request,
        "accounts/user_management.html",
        {"users": users}
    )





@login_required
def approve_user(request, user_id):
    if request.user.role != User.Role.ADMIN:
        messages.error(request, "You are not authorized to manage users.")
        return redirect("user_dashboard")

    if request.method != "POST":
        return redirect("user_management")

    account = get_object_or_404(User, id=user_id)

    if account.role == User.Role.ADMIN:
        messages.error(request, "Admin accounts cannot be approved here.")

    elif account.is_approved:
        messages.error(request, "This user is already approved.")

    else:
        account.is_approved = True
        account.is_active = True
        account.save(update_fields=["is_approved", "is_active"])

        messages.success(
            request,
            f"User '{account.username}' approved as "
            f"{account.get_role_display()}."
        )

    return redirect("user_management")



@login_required
def reject_user(request, user_id):
    if request.user.role != User.Role.ADMIN:
        messages.error(request, "You are not authorized to manage users.")
        return redirect("user_dashboard")

    if request.method != "POST":
        return redirect("user_management")

    account = get_object_or_404(User, id=user_id)

    if account.role == User.Role.ADMIN:
        messages.error(request, "Admin accounts cannot be rejected here.")
    elif account.is_approved:
        messages.error(request, "Only pending users can be rejected.")
    else:
        account.is_active = False
        account.save(update_fields=["is_active"])
        messages.success(
            request,
            f"Registration for '{account.username}' has been rejected."
        )

    return redirect("user_management")
