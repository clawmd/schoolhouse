from django.db import models


class Guest(models.Model):
    DESIRABILITY_CHOICES = [
        ('Great', 'Great'),
        ('OK', 'OK'),
        ('Bad', 'Bad'),
        ('Do Not Rent', 'Do Not Rent'),
    ]
    TITLE_CHOICES = [('Mr.', 'Mr.'), ('Mrs.', 'Mrs.'), ('Ms.', 'Ms.')]

    title = models.CharField(max_length=10, choices=TITLE_CHOICES, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_initial = models.CharField(max_length=5, blank=True)
    partner_name = models.CharField(max_length=200, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True, default='USA')
    phone_home = models.CharField(max_length=30, blank=True)
    phone_cell = models.CharField(max_length=30, blank=True)
    phone_cell2 = models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    email2 = models.EmailField(blank=True)
    pin = models.CharField(max_length=4, blank=True)
    desirability = models.CharField(max_length=20, choices=DESIRABILITY_CHOICES, blank=True)
    notes = models.TextField(blank=True)
    ha_name = models.CharField(max_length=200, blank=True, verbose_name='HA Name')
    ha_reservation = models.CharField(max_length=200, blank=True, verbose_name='HA Reservation #')
    ha_email = models.EmailField(blank=True, verbose_name='HA Email')
    ha_phone = models.CharField(max_length=30, blank=True, verbose_name='HA Phone')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        # Auto-set PIN from last 4 digits of cell phone
        if self.phone_cell and len(self.phone_cell) >= 4:
            digits = ''.join(c for c in self.phone_cell if c.isdigit())
            if len(digits) >= 4:
                self.pin = digits[-4:]
        super().save(*args, **kwargs)

    def has_duplicate_name(self):
        return Guest.objects.filter(
            first_name__iexact=self.first_name,
            last_name__iexact=self.last_name
        ).exclude(pk=self.pk).exists()

    def has_duplicate_address(self):
        if not self.address1:
            return False
        return Guest.objects.filter(
            address1__iexact=self.address1
        ).exclude(pk=self.pk).exists()

    def desirability_color(self):
        return {
            'Great': 'success',
            'OK': 'warning',
            'Bad': 'danger',
            'Do Not Rent': 'danger',
        }.get(self.desirability, 'secondary')
