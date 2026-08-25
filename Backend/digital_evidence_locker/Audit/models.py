from django.conf import settings
from django.db import models


class AuditLog(models.Model):

    ACTION_CHOICES = [
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("VIEW", "View"),
        ("UPLOAD", "Upload"),
        ("DOWNLOAD", "Download"),
        ("VERIFY", "Verify"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs"
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )

    description = models.TextField()

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    case_id = models.IntegerField(
        null=True,
        blank=True
    )

    evidence_id = models.IntegerField(
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        username = self.user.username if self.user else "Unknown User"
        return f"{username} - {self.action} - {self.timestamp}"