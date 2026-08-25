from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "action",
        "case_id",
        "evidence_id",
        "ip_address",
        "timestamp",
    )

    list_filter = (
        "action",
        "timestamp",
    )

    search_fields = (
        "user__username",
        "description",
        "case_id",
        "evidence_id",
    )

    readonly_fields = (
        "timestamp",
    )