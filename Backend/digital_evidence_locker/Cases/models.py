from django.conf import settings
from django.db import models


class Case(models.Model):

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        UNDER_INVESTIGATION = "UNDER_INVESTIGATION", "Under Investigation"
        FORENSIC_ANALYSIS = "FORENSIC_ANALYSIS", "Forensic Analysis"
        SUBMITTED_TO_COURT = "SUBMITTED_TO_COURT", "Submitted to Court"
        CLOSED = "CLOSED", "Closed"

    case_number = models.CharField(
        max_length=50,
        unique=True
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.OPEN
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_cases"
    )

    assigned_investigator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_cases"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    closed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.case_number} - {self.title}"