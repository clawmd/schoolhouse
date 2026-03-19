from django.db import models


class Month(models.Model):
    year = models.PositiveIntegerField()
    month_number = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_date_paid = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', '-month_number']
        unique_together = ('year', 'month_number')

    def __str__(self):
        month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        return f'{month_names[self.month_number - 1]} {self.year}'
