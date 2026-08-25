from django.conf import settings
from django.db import models


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        INFO = "INFO", "Information"
        SUCCESS = "SUCCESS", "Success"
        WARNING = "WARNING", "Warning"
        SECURITY = "SECURITY", "Security Alert"
        BLOCKCHAIN = "BLOCKCHAIN", "Blockchain Alert"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.INFO
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    read_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.recipient.username}"