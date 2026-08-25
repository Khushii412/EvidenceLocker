from django import forms

from .models import Notification


class NotificationForm(forms.ModelForm):

    class Meta:
        model = Notification

        fields = [
            "recipient",
            "title",
            "message",
            "notification_type",
        ]

        widgets = {
            "recipient": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Notification title"
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Notification message"
                }
            ),

            "notification_type": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
        }