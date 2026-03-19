from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import AppSettings
from .forms import AppSettingsForm


@login_required
def dashboard(request):
    from reservations.models import Reservation
    from maintenance.models import MaintenanceTask
    from issues.models import Issue
    today = timezone.now().date()

    current = Reservation.objects.select_related('guest').filter(
        arrive_date__lte=today, leave_date__gte=today
    ).first()

    upcoming = Reservation.objects.select_related('guest').filter(
        arrive_date__gt=today
    ).order_by('arrive_date')[:8]

    overdue_payments = []
    for r in Reservation.objects.select_related('guest').filter(
        arrive_date__gt=today
    ).order_by('arrive_date'):
        if r.pay_1_overdue() or r.pay_2_overdue():
            overdue_payments.append(r)

    open_issues = Issue.objects.filter(completion_date__isnull=True).count()
    open_maintenance = MaintenanceTask.objects.filter(status='To Do').count()

    return render(request, 'core/dashboard.html', {
        'current': current,
        'upcoming': upcoming,
        'overdue_payments': overdue_payments,
        'open_issues': open_issues,
        'open_maintenance': open_maintenance,
        'today': today,
    })


@login_required
def settings_view(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access settings.')
        return redirect('reservations:list')
    obj = AppSettings.get()
    if request.method == 'POST':
        form = AppSettingsForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings saved.')
            return redirect('core:settings')
    else:
        form = AppSettingsForm(instance=obj)
    return render(request, 'core/settings.html', {'form': form})
