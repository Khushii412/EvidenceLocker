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
        return redirect("admin_dashboard")

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
    Admin dashboard.
    Only users with ADMIN role can access it.
    """

    if request.user.role != User.Role.ADMIN:
        messages.error(
            request,
            "You are not authorized to access the Admin Dashboard."
        )
        return redirect("user_dashboard")

    context = {
        "total_users": User.objects.count(),
        "approved_users": User.objects.filter(
            is_approved=True
        ).count(),
        "pending_users": User.objects.filter(
            is_approved=False
        ).count(),
        "active_users": User.objects.filter(
            is_active=True
        ).count(),
    }

    return render(
        request,
        "admin/dashboard.html",
        context
    )


@login_required
def user_dashboard(request):
    """
    Temporary dashboard for non-admin users.
    Later this will redirect users to their respective dashboards.
    """

    return render(
        request,
        "accounts/user_dashboard.html"
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
        selected_role = request.POST.get("role")

        allowed_roles = {
            User.Role.INVESTIGATOR,
            User.Role.FORENSIC_EXPERT,
            User.Role.JUDGE,
        }

        if selected_role not in allowed_roles:
            messages.error(request, "Please select a valid role.")
        else:
            account.role = selected_role
            account.is_approved = True
            account.is_active = True
            account.save(
                update_fields=["role", "is_approved", "is_active"]
            )

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
