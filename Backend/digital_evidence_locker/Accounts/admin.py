from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "email",
        "role",
        "is_approved",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "role",
        "is_approved",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Digital Evidence Locker Information",
            {
                "fields": (
                    "role",
                    "is_approved",
                    "profile_image",
                    "phone_number",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Digital Evidence Locker Information",
            {
                "fields": (
                    "role",
                    "is_approved",
                    "profile_image",
                    "phone_number",
                )
            },
        ),
    )