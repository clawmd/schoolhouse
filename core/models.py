from django.db import models


class AppSettings(models.Model):
    """Singleton settings table — only one row allowed."""
    owner_first_name = models.CharField(max_length=100, blank=True)
    owner_last_name = models.CharField(max_length=100, blank=True)
    owner_middle_initial = models.CharField(max_length=10, blank=True)
    owner_email = models.EmailField(blank=True)
    owner_phone = models.CharField(max_length=30, blank=True)
    owner_address1 = models.CharField(max_length=200, blank=True)
    owner_address2 = models.CharField(max_length=200, blank=True)
    owner_city = models.CharField(max_length=100, blank=True)
    owner_state = models.CharField(max_length=50, blank=True)
    owner_zip = models.CharField(max_length=20, blank=True)
    owner_country = models.CharField(max_length=100, blank=True, default='USA')
    google_phone = models.CharField(max_length=30, blank=True)
    email_agent = models.EmailField(blank=True)
    salutation = models.TextField(blank=True)
    closing = models.TextField(blank=True)
    email_confirmation_body = models.TextField(blank=True)
    ein = models.CharField(max_length=50, blank=True)
    state_tax_reg_number = models.CharField(max_length=50, blank=True)
    state_occupancy_tax_number = models.CharField(max_length=50, blank=True)
    paypal = models.CharField(max_length=200, blank=True)
    amazon_prime = models.CharField(max_length=200, blank=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=4, default='0.1500')
    mileage_rate = models.DecimalField(max_digits=5, decimal_places=4, default='0.5400')
    service_types = models.TextField(blank=True, help_text='One service type per line')
    maintenance_types = models.TextField(blank=True, help_text='One maintenance type per line')

    class Meta:
        verbose_name = 'App Settings'
        verbose_name_plural = 'App Settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'App Settings'

    def service_type_list(self):
        return [s.strip() for s in self.service_types.splitlines() if s.strip()]

    def maintenance_type_list(self):
        return [s.strip() for s in self.maintenance_types.splitlines() if s.strip()]
