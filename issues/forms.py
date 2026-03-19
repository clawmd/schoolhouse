from django import forms
from .models import Issue


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'note', 'priority', 'needs_attention', 'completion_date']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 4}),
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
        }
