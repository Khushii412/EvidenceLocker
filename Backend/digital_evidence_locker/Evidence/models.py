import hashlib

from django.conf import settings
from django.db import models

from Cases.models import Case


class Evidence(models.Model):

    class Status(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Submitted"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        VERIFIED = "VERIFIED", "Verified"
        REJECTED = "REJECTED", "Rejected"

    case = models.ForeignKey(
        Case,
        on_delete=models.PROTECT,
        related_name="evidence"
    )

    evidence_number = models.CharField(
        max_length=100,
        unique=True
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    file = models.FileField(
        upload_to="evidence/"
    )

    file_hash = models.CharField(
        max_length=64,
        blank=True,
        editable=False
    )

    blockchain_tx_hash = models.CharField(
    max_length=66,
    blank=True,
    editable=False
    )

    blockchain_block_number = models.PositiveBigIntegerField(
    null=True,
    blank=True,
    editable=False
    )

    blockchain_timestamp = models.DateTimeField(
        null=True,
        blank=True,
        editable=False
    )

    file_size = models.PositiveBigIntegerField(
        default=0,
        editable=False
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="uploaded_evidence"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def calculate_hash(self):
        sha256 = hashlib.sha256()

        self.file.seek(0)

        for chunk in self.file.chunks():
            sha256.update(chunk)

        self.file.seek(0)

        return sha256.hexdigest()

    def save(self, *args, **kwargs):

        if self.file:
            self.file_size = self.file.size
            self.file_hash = self.calculate_hash()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.evidence_number} - {self.title}"

class EvidenceActivity(models.Model):

    class Action(models.TextChoices):
        UPLOADED = "UPLOADED", "Uploaded"
        VIEWED = "VIEWED", "Viewed"
        VERIFIED = "VERIFIED", "Verified"
        REJECTED = "REJECTED", "Rejected"
        DOWNLOADED = "DOWNLOADED", "Downloaded"
        MODIFIED = "MODIFIED", "Modified"

    evidence = models.ForeignKey(
        Evidence,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="evidence_activities"
    )

    action = models.CharField(
        max_length=20,
        choices=Action.choices
    )

    description = models.TextField(
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.evidence.evidence_number} - {self.action}"