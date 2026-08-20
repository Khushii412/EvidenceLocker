from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

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
