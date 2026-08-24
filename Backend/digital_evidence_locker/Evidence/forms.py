from django import forms

from .models import Evidence


class EvidenceForm(forms.ModelForm):

    class Meta:
        model = Evidence

        fields = [
            "case",
            "evidence_number",
            "title",
            "description",
            "file",
        ]

        widgets = {
            "case": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "evidence_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter evidence number"
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter evidence title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter evidence description"
                }
            ),

            "file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }