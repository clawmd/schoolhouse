from django.db import models
from django.utils import timezone
from guests.models import Guest


class Rate(models.Model):
    SEASON_CHOICES = [
        ('Summer', 'Summer'), ('Spring', 'Spring'), ('Fall', 'Fall'),
        ('Early Spring', 'Early Spring'), ('Late Spring', 'Late Spring'),
    ]
    season = models.CharField(max_length=50, choices=SEASON_CHOICES, blank=True)
    date_start = models.DateField()
    date_end = models.DateField()
    rate_weekly = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rate_daily = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rate_weekly_cc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Weekly Rate (CC)')
    rate_daily_cc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Daily Rate (CC)')
    deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cleaning = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_start']

    def __str__(self):
        return f'{self.season} ({self.date_start} – {self.date_end})'


class Reservation(models.Model):
    SOURCE_CHOICES = [
        ('Prior', 'Prior Guest'), ('HA', 'HomeAway/VRBO'), ('VRBO', 'VRBO'),
        ('Agent', 'Agent'), ('Website', 'Website'), ('Guest', 'Guest Referral'), ('Other', 'Other'),
    ]
    PAYMENT_TYPE_CHOICES = [
        ('Check', 'Check'), ('Credit Card', 'Credit Card'), ('Cash', 'Cash'),
        ('PayPal', 'PayPal'), ('Venmo', 'Venmo'), ('Amazon', 'Amazon'),
    ]
    CONTRACT_CHOICES = [('1', '1 Payment'), ('2', '2 Payments'), ('HA', 'HomeAway')]
    CONTRACT_STATUS_CHOICES = [('Sent', 'Sent'), ('Signed', 'Signed')]

    guest = models.ForeignKey(Guest, on_delete=models.PROTECT)
    arrive_date = models.DateField()
    leave_date = models.DateField()
    arrive_time = models.TimeField(null=True, blank=True)
    leave_time = models.TimeField(null=True, blank=True)
    adults_count = models.PositiveIntegerField(default=1)
    children_count = models.PositiveIntegerField(default=0)
    pets = models.BooleanField(default=False)
    other = models.CharField(max_length=200, blank=True)
    other_needs = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, blank=True)
    season = models.CharField(max_length=50, blank=True)
    # fees
    rental_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cleaning_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    additional_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    additional_fee_note = models.CharField(max_length=200, blank=True)
    tax_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # payments
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES, blank=True)
    payment_contract_how_many = models.CharField(max_length=5, choices=CONTRACT_CHOICES, blank=True)
    payment_1_actual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_1_date = models.DateField(null=True, blank=True)
    payment_1_note = models.TextField(blank=True)
    payment_1_deposit = models.CharField(max_length=50, blank=True)
    payment_2_actual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_2_date = models.DateField(null=True, blank=True)
    payment_2_note = models.TextField(blank=True)
    payment_2_deposit = models.CharField(max_length=50, blank=True)
    payment_deposit_received = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deposit_amount_returned = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deposit_returned = models.BooleanField(default=False)
    # status tracking
    confirm_sent = models.BooleanField(default=False)
    precheck_email_sent = models.BooleanField(default=False)
    contract_rules_sent = models.BooleanField(default=False)
    contract_rules_status = models.CharField(max_length=20, choices=CONTRACT_STATUS_CHOICES, blank=True)
    contract_pet_sent = models.BooleanField(default=False)
    contract_pet_status = models.CharField(max_length=20, choices=CONTRACT_STATUS_CHOICES, blank=True)
    # pin
    pin = models.CharField(max_length=10, blank=True)
    # ha fields
    ha_reservation = models.CharField(max_length=200, blank=True)
    ha_name = models.CharField(max_length=200, blank=True)
    ha_checkin = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-arrive_date']

    def __str__(self):
        return f'{self.guest} — {self.arrive_date}'

    def number_of_nights(self):
        return (self.leave_date - self.arrive_date).days

    def total_fee(self):
        return (self.rental_fee or 0) + (self.cleaning_fee or 0) + (self.additional_fee or 0)

    def balance(self):
        paid = (self.payment_1_actual or 0) + (self.payment_2_actual or 0)
        return self.total_fee() - paid

    def status(self):
        now = timezone.now().date()
        if now < self.arrive_date:
            return 'pending'
        elif now > self.leave_date:
            return 'expired'
        return 'current'

    def status_color(self):
        return {'pending': 'warning', 'current': 'success', 'expired': 'secondary'}.get(self.status(), 'secondary')

    def pay_1_due(self):
        from datetime import timedelta
        return self.arrive_date + timedelta(days=7)

    def pay_2_due(self):
        from datetime import timedelta
        return self.arrive_date - timedelta(days=30)

    def pay_1_overdue(self):
        return (not self.payment_1_actual) and timezone.now().date() > self.pay_1_due()

    def pay_2_overdue(self):
        return (not self.payment_2_actual) and timezone.now().date() > self.pay_2_due()

    def has_overlap(self):
        return Reservation.objects.filter(
            arrive_date__lt=self.leave_date,
            leave_date__gt=self.arrive_date,
        ).exclude(pk=self.pk).exists()

    def save(self, *args, **kwargs):
        if self.guest and self.guest.pin:
            self.pin = self.guest.pin
        super().save(*args, **kwargs)
