from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models.deletion import ProtectedError
from .forms import CaseForm
from .models import Case
from Audit.models import AuditLog
from functools import wraps
from django.core.exceptions import PermissionDenied




def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                raise PermissionDenied(
                    "You do not have permission to access this page."
                )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


@role_required("ADMIN", "INVESTIGATOR", "FORENSIC_EXPERT", "JUDGE")
def case_list(request):
    cases = Case.objects.select_related(
        "created_by",
        "assigned_investigator"
    )

    return render(
        request,
        "cases/case_list.html",
        {"cases": cases}
    )


@role_required("ADMIN", "INVESTIGATOR", "FORENSIC_EXPERT", "JUDGE")
def case_detail(request, case_id):
    case = get_object_or_404(
        Case.objects.select_related(
            "created_by",
            "assigned_investigator"
        ),
        id=case_id
    )
    AuditLog.objects.create(
        user=request.user,
        action="VIEW",
        description=f"Case {case.case_number} viewed.",
        ip_address=request.META.get("REMOTE_ADDR"),
        case_id=case.id
        )

    return render(
        request,
        "cases/case_detail.html",
        {"case": case}
    )


@role_required("ADMIN", "INVESTIGATOR")
def create_case(request):

    if request.method == "POST":
        form = CaseForm(request.POST)

        if form.is_valid():
            case = form.save(commit=False)
            case.created_by = request.user
            case.save()

            AuditLog.objects.create(
                user=request.user,
                action="VIEW",
                description=f"Case {case.case_number} viewed.",
                ip_address=request.META.get("REMOTE_ADDR"),
                case_id=case.id
            )

            messages.success(
                request,
                "Case created successfully."
            )

            return redirect("cases:case_detail", case_id=case.id)

    else:
        form = CaseForm()

    return render(
        request,
        "cases/case_form.html",
        {
            "form": form,
            "page_title": "Create Case"
        }
    )


@role_required("ADMIN", "INVESTIGATOR")
def edit_case(request, case_id):

    case = get_object_or_404(Case, id=case_id)

    if request.method == "POST":
        form = CaseForm(
            request.POST,
            instance=case
        )

        if form.is_valid():
            form.save()

            AuditLog.objects.create(
                user=request.user,
                action="UPDATE",
                description=f"Case {case.case_number} updated.",
                ip_address=request.META.get("REMOTE_ADDR"),
                case_id=case.id
            )

            messages.success(
                request,
                "Case updated successfully."
            )

            return redirect(
                "cases:case_detail",
                case_id=case.id
            )

    else:
        form = CaseForm(instance=case)

    return render(
        request,
        "cases/case_form.html",
        {
            "form": form,
            "page_title": "Edit Case"
        }
    )



@role_required("ADMIN")
def delete_case(request, case_id):

    case = get_object_or_404(Case, id=case_id)

    if request.method == "POST":

        try:
            case.delete()

            messages.success(
                request,
                "Case deleted successfully."
            )

            return redirect("cases:case_list")

        except ProtectedError:
            messages.error(
                request,
                "This case cannot be deleted because it contains evidence."
            )

            return redirect(
                "cases:case_detail",
                case_id=case.id
            )

    return render(
        request,
        "cases/case_confirm_delete.html",
        {"case": case}
    )