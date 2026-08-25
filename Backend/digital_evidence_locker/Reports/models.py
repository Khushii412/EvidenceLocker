from django.conf import settings
from django.db import models


class Report(models.Model):

    REPORT_TYPE_CHOICES = [
        ("CASE", "Case Report"),
        ("FORENSIC", "Forensic Report"),
        ("EVIDENCE", "Evidence Report"),
    ]

    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("FINAL", "Final"),
    ]

    title = models.CharField(max_length=255)

    report_type = models.CharField(
        max_length=20,
        choices=REPORT_TYPE_CHOICES
    )

    case_id = models.IntegerField(
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reports"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="DRAFT"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title
