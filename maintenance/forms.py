from django import forms
from .models import MaintenanceTask


class MaintenanceTaskForm(forms.ModelForm):
    class Meta:
        model = MaintenanceTask
        fields = ['title', 'type', 'note', 'priority', 'status', 'frequency_days', 'frequency_months', 'completed_date']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
            'completed_date': forms.DateInput(attrs={'type': 'date'}),
        }
