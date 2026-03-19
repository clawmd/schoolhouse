from django.db import models
from datetime import timedelta


class MaintenanceTask(models.Model):
    PRIORITY_CHOICES = [('low', 'Low'), ('med', 'Medium'), ('high', 'High'), ('critical', 'Critical')]
    STATUS_CHOICES = [('To Do', 'To Do'), ('Done', 'Done')]

    title = models.CharField(max_length=200)
    type = models.CharField(max_length=100, blank=True)
    note = models.TextField(blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='To Do')
    frequency_days = models.PositiveIntegerField(null=True, blank=True)
    frequency_months = models.PositiveIntegerField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['status', '-created_at']

    def __str__(self):
        return self.title

    def due_date(self):
        if self.completed_date and self.frequency_days:
            return self.completed_date + timedelta(days=self.frequency_days)
        return None
