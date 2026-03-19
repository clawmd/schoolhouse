from django.db import models


class Expense(models.Model):
    TAX_CATEGORY_CHOICES = [
        ('Capital Improvement', 'Capital Improvement'),
        ('Insurance', 'Insurance'),
        ('Maintenance', 'Maintenance'),
        ('Tax', 'Tax'),
        ('Travel', 'Travel'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'), ('Cash', 'Cash'), ('Check', 'Check'),
        ('Amazon', 'Amazon'), ('PayPal', 'PayPal'), ('Venmo', 'Venmo'),
    ]

    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_category = models.CharField(max_length=50, choices=TAX_CATEGORY_CHOICES, blank=True)
    note = models.TextField(blank=True)
    expense_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, blank=True)
    receipt = models.ImageField(upload_to='receipts/', null=True, blank=True)
    maintenance_trip = models.BooleanField(default=False)
    miles = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    meal_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.CharField(max_length=50, blank=True)
    order_number = models.CharField(max_length=100, blank=True)
    cost_per = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    replaced_broken = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-expense_date', '-created_at']

    def __str__(self):
        return self.title

    def miles_amount(self, mileage_rate=None):
        if not self.miles:
            return None
        if mileage_rate is None:
            from core.models import AppSettings
            mileage_rate = AppSettings.get().mileage_rate
        return round(float(self.miles) * float(mileage_rate), 2)
