from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models.deletion import ProtectedError
from .forms import CaseForm
from .models import Case
from Audit.models import AuditLog
from functools import wraps
from django.core.exceptions import PermissionDenied
from Accounts.models import User




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
        "assigned_investigator",
        "assigned_forensic_expert",
        "assigned_judge",
    )

    if request.user.role == User.Role.ADMIN:
        pass
    elif request.user.role == User.Role.INVESTIGATOR:
        cases = cases.filter(assigned_investigator=request.user)
    elif request.user.role == User.Role.FORENSIC_EXPERT:
        cases = cases.filter(assigned_forensic_expert=request.user)
    elif request.user.role == User.Role.JUDGE:
        cases = cases.filter(assigned_judge=request.user)

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
            "assigned_investigator",
            "assigned_forensic_expert",
            "assigned_judge",
        ),
        id=case_id
    )

    # Check whether this user is assigned to the case.
    if request.user.role == User.Role.INVESTIGATOR:
        authorized = case.assigned_investigator_id == request.user.id
    elif request.user.role == User.Role.FORENSIC_EXPERT:
        authorized = case.assigned_forensic_expert_id == request.user.id
    elif request.user.role == User.Role.JUDGE:
        authorized = case.assigned_judge_id == request.user.id
    else:
        authorized = True  # Admin

    if not authorized:
        raise PermissionDenied(
            "You are not authorized to view this case."
        )

    AuditLog.objects.create(
        user=request.user,
        action="VIEW",
        description=f"Case {case.case_number} viewed.",
        ip_address=request.META.get("REMOTE_ADDR"),
        case_id=case.id
    )

    status_choices = Case.Status.choices

    return render(
        request,
        "cases/case_detail.html",
        {"case": case, "status_choices": status_choices}
    )



@role_required("ADMIN", "INVESTIGATOR")
def create_case(request):
    if request.method == "POST":
        form = CaseForm(request.POST)

        if form.is_valid():
            case = form.save(commit=False)
            case.created_by = request.user

            # Admins can assign all roles.
            # Investigators are automatically assigned to cases they create.
            if request.user.role == User.Role.INVESTIGATOR:
                case.assigned_investigator = request.user
                case.assigned_forensic_expert = None
                case.assigned_judge = None

            case.save()

            AuditLog.objects.create(
                user=request.user,
                action="CREATE",
                description=f"Case {case.case_number} created.",
                ip_address=request.META.get("REMOTE_ADDR"),
                case_id=case.id
            )

            messages.success(request, "Case created successfully.")
            return redirect("cases:case_detail", case_id=case.id)

    else:
        form = CaseForm()

    if request.user.role != User.Role.ADMIN:
        for field in (
            "assigned_investigator",
            "assigned_forensic_expert",
            "assigned_judge",
        ):
            form.fields[field].disabled = True

    return render(
        request,
        "cases/case_form.html",
        {"form": form, "page_title": "Create Case"}
    )


@role_required("ADMIN", "INVESTIGATOR")
def edit_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)

    if (
        request.user.role == User.Role.INVESTIGATOR
        and case.assigned_investigator_id != request.user.id
    ):
        raise PermissionDenied(
            "You are not authorized to edit this case."
        )

    if request.method == "POST":
        form = CaseForm(request.POST, instance=case)

        if form.is_valid():
            updated_case = form.save(commit=False)

            # Preserve assignments submitted by Admin only.
            if request.user.role != User.Role.ADMIN:
                updated_case.assigned_investigator = case.assigned_investigator
                updated_case.assigned_forensic_expert = case.assigned_forensic_expert
                updated_case.assigned_judge = case.assigned_judge

            updated_case.save()

            AuditLog.objects.create(
                user=request.user,
                action="UPDATE",
                description=f"Case {case.case_number} updated.",
                ip_address=request.META.get("REMOTE_ADDR"),
                case_id=case.id
            )

            messages.success(request, "Case updated successfully.")
            return redirect("cases:case_detail", case_id=case.id)

    else:
        form = CaseForm(instance=case)

    if request.user.role != User.Role.ADMIN:
        for field in (
            "assigned_investigator",
            "assigned_forensic_expert",
            "assigned_judge",
        ):
            form.fields[field].disabled = True

    return render(
        request,
        "cases/case_form.html",
        {"form": form, "page_title": "Edit Case"}
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




@role_required("ADMIN", "INVESTIGATOR", "FORENSIC_EXPERT", "JUDGE")
def update_case_status(request, case_id):
    if request.method != "POST":
        return redirect("cases:case_detail", case_id=case_id)

    case = get_object_or_404(Case, id=case_id)
    new_status = request.POST.get("status")

    # Admin can change any case status.
    if request.user.role == User.Role.ADMIN:
        allowed = True

    # Investigator can start investigation or submit to court.
    elif request.user.role == User.Role.INVESTIGATOR:
        allowed = (
            case.assigned_investigator_id == request.user.id
            and (
                (
                    case.status == Case.Status.OPEN
                    and new_status == Case.Status.UNDER_INVESTIGATION
                )
                or (
                    case.status == Case.Status.FORENSIC_ANALYSIS
                    and new_status == Case.Status.SUBMITTED_TO_COURT
                )
            )
        )

    # Forensic Expert can begin forensic analysis.
    elif request.user.role == User.Role.FORENSIC_EXPERT:
        allowed = (
            case.assigned_forensic_expert_id == request.user.id
            and case.status == Case.Status.UNDER_INVESTIGATION
            and new_status == Case.Status.FORENSIC_ANALYSIS
        )

    # Judge can close a case submitted to court.
    elif request.user.role == User.Role.JUDGE:
        allowed = (
            case.assigned_judge_id == request.user.id
            and case.status == Case.Status.SUBMITTED_TO_COURT
            and new_status == Case.Status.CLOSED
        )

    else:
        allowed = False

    # Reject invalid transitions and unauthorized changes.
    if not allowed:
        messages.error(
            request,
            "You are not authorized to make this status change."
        )
        return redirect("cases:case_detail", case_id=case.id)

    # Validate the status value.
    valid_statuses = Case.Status.values
    if new_status not in valid_statuses:
        messages.error(request, "Invalid case status.")
        return redirect("cases:case_detail", case_id=case.id)

    old_status = case.status
    case.status = new_status

    if new_status == Case.Status.CLOSED:
        from django.utils import timezone
        case.closed_at = timezone.now()
    else:
        case.closed_at = None

    case.save()

    AuditLog.objects.create(
        user=request.user,
        action="UPDATE",
        description=(
            f"Case {case.case_number} status changed "
            f"from {old_status} to {new_status}."
        ),
        ip_address=request.META.get("REMOTE_ADDR"),
        case_id=case.id,
    )

    messages.success(request, "Case status updated successfully.")
    return redirect("cases:case_detail", case_id=case.id)
