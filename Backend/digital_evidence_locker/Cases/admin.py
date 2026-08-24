from django.contrib import admin
from .models import Case


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):

    list_display = (
        "case_number",
        "title",
        "status",
        "created_by",
        "assigned_investigator",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "case_number",
        "title",
        "description",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )