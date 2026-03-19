from django import forms
from .models import Guest


class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = [
            'title', 'first_name', 'last_name', 'middle_initial', 'partner_name',
            'address1', 'address2', 'city', 'state', 'zip_code', 'country',
            'phone_home', 'phone_cell', 'phone_cell2',
            'email', 'email2', 'pin', 'desirability', 'notes',
            'ha_name', 'ha_reservation', 'ha_email', 'ha_phone',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
