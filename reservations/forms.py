from django import forms
from .models import Reservation, Rate


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'guest', 'arrive_date', 'leave_date', 'arrive_time', 'leave_time',
            'adults_count', 'children_count', 'pets', 'notes', 'other_needs',
            'source', 'season',
            'rental_fee', 'cleaning_fee', 'additional_fee', 'additional_fee_note',
            'tax_fee', 'deposit',
            'payment_type', 'payment_contract_how_many',
            'payment_1_actual', 'payment_1_date', 'payment_1_note', 'payment_1_deposit',
            'payment_2_actual', 'payment_2_date', 'payment_2_note', 'payment_2_deposit',
            'payment_deposit_received', 'deposit_amount_returned', 'deposit_returned',
            'confirm_sent', 'precheck_email_sent',
            'contract_rules_sent', 'contract_rules_status',
            'contract_pet_sent', 'contract_pet_status',
            'ha_reservation', 'ha_name', 'ha_checkin',
        ]
        widgets = {
            'arrive_date': forms.DateInput(attrs={'type': 'date'}),
            'leave_date': forms.DateInput(attrs={'type': 'date'}),
            'arrive_time': forms.TimeInput(attrs={'type': 'time'}),
            'leave_time': forms.TimeInput(attrs={'type': 'time'}),
            'payment_1_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_2_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'other_needs': forms.Textarea(attrs={'rows': 2}),
            'payment_1_note': forms.Textarea(attrs={'rows': 2}),
            'payment_2_note': forms.Textarea(attrs={'rows': 2}),
        }


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ['season', 'date_start', 'date_end', 'rate_weekly', 'rate_daily',
                  'rate_weekly_cc', 'rate_daily_cc', 'deposit', 'cleaning']
        widgets = {
            'date_start': forms.DateInput(attrs={'type': 'date'}),
            'date_end': forms.DateInput(attrs={'type': 'date'}),
        }
