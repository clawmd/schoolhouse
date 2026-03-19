from django.db import models


class Contact(models.Model):
    company = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    phone_office = models.CharField(max_length=30, blank=True)
    phone_home = models.CharField(max_length=30, blank=True)
    phone_cell = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    email2 = models.EmailField(blank=True)
    service_type = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name', 'company']

    def __str__(self):
        if self.last_name:
            return f'{self.last_name}, {self.first_name}' + (f' ({self.company})' if self.company else '')
        return self.company or 'Contact'
