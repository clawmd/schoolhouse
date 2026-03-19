from django import forms
from .models import AppSettings


class AppSettingsForm(forms.ModelForm):
    class Meta:
        model = AppSettings
        exclude = []
        widgets = {
            'email_confirmation_body': forms.Textarea(attrs={'rows': 6}),
            'salutation': forms.Textarea(attrs={'rows': 3}),
            'closing': forms.Textarea(attrs={'rows': 3}),
            'service_types': forms.Textarea(attrs={'rows': 5, 'placeholder': 'One type per line'}),
            'maintenance_types': forms.Textarea(attrs={'rows': 5, 'placeholder': 'One type per line'}),
        }
