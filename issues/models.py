from django.db import models
from django.contrib.auth.models import User


class Issue(models.Model):
    PRIORITY_CHOICES = [('low', 'Low'), ('med', 'Medium'), ('high', 'High'), ('critical', 'Critical')]

    title = models.CharField(max_length=200)
    note = models.TextField(blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, blank=True)
    needs_attention = models.BooleanField(default=False)
    completion_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_open(self):
        return self.completion_date is None
