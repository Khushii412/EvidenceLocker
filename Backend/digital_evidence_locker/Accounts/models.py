from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        INVESTIGATOR = "INVESTIGATOR", "Investigator"
        FORENSIC_EXPERT = "FORENSIC_EXPERT", "Forensic Expert"
        JUDGE = "JUDGE", "Judge"

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.INVESTIGATOR,
    )

    is_approved = models.BooleanField(default=False)

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"