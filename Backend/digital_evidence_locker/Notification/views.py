from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Notification


@login_required
def notification_list(request):

    notifications = Notification.objects.filter(
        recipient=request.user
    )

    return render(
        request,
        "notifications/notification_list.html",
        {
            "notifications": notifications
        }
    )


@login_required
def mark_as_read(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user
    )

    notification.is_read = True
    notification.read_at = timezone.now()
    notification.save(
        update_fields=["is_read", "read_at"]
    )

    return redirect("notifications:notification_list")


@login_required
def mark_all_as_read(request):

    Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(
        is_read=True,
        read_at=timezone.now()
    )

    return redirect("notifications:notification_list")