from django.db import models
from guests.models import Guest


class Document(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True, blank=True)
    reservation_id = models.PositiveIntegerField(null=True, blank=True)
    email_recipient = models.EmailField(blank=True)
    email_subject = models.CharField(max_length=200, blank=True)
    email_salutation = models.TextField(blank=True)
    email_body = models.TextField(blank=True)
    email_closing = models.TextField(blank=True)
    email_sig = models.TextField(blank=True)
    email_letter = models.TextField(blank=True)
    created_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email_subject or f'Document #{self.pk}'
