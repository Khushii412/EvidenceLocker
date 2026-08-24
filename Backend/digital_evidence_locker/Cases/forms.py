from django import forms
from .models import Case
from Accounts.models import User


class CaseForm(forms.ModelForm):

    class Meta:
        model = Case
        fields = [
            "case_number",
            "title",
            "description",
            "assigned_investigator",
        ]

        widgets = {
            "case_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter case number"
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter case title"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter case description"
                }
            ),
            "assigned_investigator": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["assigned_investigator"].queryset = User.objects.filter(
            role=User.Role.INVESTIGATOR,
            is_approved=True,
            is_active=True
        )

        self.fields["assigned_investigator"].required = False