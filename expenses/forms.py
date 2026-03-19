from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'title', 'amount', 'tax_category', 'expense_date', 'payment_method',
            'replaced_broken', 'maintenance_trip', 'miles',
            'meal_amount', 'quantity', 'order_number', 'cost_per',
            'receipt', 'note',
        ]
        widgets = {
            'expense_date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }
