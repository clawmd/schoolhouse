from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'company', 'first_name', 'last_name',
            'address1', 'address2', 'city', 'state', 'zip_code',
            'phone_office', 'phone_home', 'phone_cell',
            'email', 'email2', 'service_type', 'website', 'notes',
        ]
        widgets = {'notes': forms.Textarea(attrs={'rows': 3})}
