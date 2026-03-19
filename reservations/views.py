import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Reservation, Rate
from .forms import ReservationForm, RateForm
from core.models import AppSettings


@login_required
def reservation_list(request):
    show = request.GET.get('show', 'upcoming')
    from django.utils import timezone
    today = timezone.now().date()
    reservations = Reservation.objects.select_related('guest').all()
    if show == 'upcoming':
        reservations = reservations.filter(leave_date__gte=today)
    elif show == 'past':
        reservations = reservations.filter(leave_date__lt=today)
    return render(request, 'reservations/list.html', {
        'reservations': reservations,
        'show': show,
    })


@login_required
def reservation_detail(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    prior_stays = Reservation.objects.filter(
        guest=res.guest,
        arrive_date__lt=res.arrive_date
    ).exclude(pk=pk).order_by('-arrive_date')[:5]
    settings = AppSettings.get()
    return render(request, 'reservations/detail.html', {
        'res': res,
        'prior_stays': prior_stays,
        'settings': settings,
    })


@login_required
def reservation_new(request):
    guest_pk = request.GET.get('guest')
    settings = AppSettings.get()
    initial = {}
    if settings.cleaning_fee:
        initial['cleaning_fee'] = settings.cleaning_fee
    if guest_pk:
        from guests.models import Guest
        try:
            initial['guest'] = Guest.objects.get(pk=guest_pk)
        except Guest.DoesNotExist:
            pass
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            res = form.save()
            messages.success(request, 'Reservation created.')
            return redirect('reservations:detail', pk=res.pk)
    else:
        form = ReservationForm(initial=initial)
    return render(request, 'reservations/form.html', {'form': form, 'title': 'New Reservation'})


@login_required
def reservation_edit(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=res)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reservation updated.')
            return redirect('reservations:detail', pk=res.pk)
    else:
        form = ReservationForm(instance=res)
    return render(request, 'reservations/form.html', {'form': form, 'res': res, 'title': 'Edit Reservation'})


@login_required
def reservation_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('reservations:list')
    res = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        res.delete()
        messages.success(request, 'Reservation deleted.')
        return redirect('reservations:list')
    return render(request, 'reservations/confirm_delete.html', {'res': res})


@login_required
def reservation_calendar(request):
    from django.utils import timezone
    reservations = Reservation.objects.select_related('guest').filter(
        leave_date__gte=timezone.now().date()
    )
    events = []
    for r in reservations:
        events.append({
            'title': str(r.guest),
            'start': str(r.arrive_date),
            'end': str(r.leave_date),
            'url': f'/reservations/{r.pk}/',
            'color': '#0d6efd' if r.status() == 'current' else '#6c757d',
        })
    return render(request, 'reservations/calendar.html', {
        'events_json': json.dumps(events),
    })


@login_required
def rate_list(request):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('reservations:list')
    rates = Rate.objects.all()
    return render(request, 'reservations/rate_list.html', {'rates': rates})


@login_required
def rate_new(request):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('reservations:list')
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rate added.')
            return redirect('reservations:rate_list')
    else:
        form = RateForm()
    return render(request, 'reservations/rate_form.html', {'form': form, 'title': 'New Rate Period'})


@login_required
def rate_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('reservations:list')
    rate = get_object_or_404(Rate, pk=pk)
    if request.method == 'POST':
        form = RateForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rate updated.')
            return redirect('reservations:rate_list')
    else:
        form = RateForm(instance=rate)
    return render(request, 'reservations/rate_form.html', {'form': form, 'rate': rate, 'title': 'Edit Rate Period'})


@login_required
def rate_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('reservations:list')
    rate = get_object_or_404(Rate, pk=pk)
    if request.method == 'POST':
        rate.delete()
        messages.success(request, 'Rate deleted.')
        return redirect('reservations:rate_list')
    return render(request, 'reservations/rate_confirm_delete.html', {'rate': rate})


def public_calendar(request):
    """Public unauthenticated calendar view."""
    reservations = Reservation.objects.all()
    events = []
    for r in reservations:
        events.append({
            'title': 'Reserved',
            'start': str(r.arrive_date),
            'end': str(r.leave_date),
            'color': '#dc3545',
            'display': 'background',
        })
    return render(request, 'reservations/public_calendar.html', {
        'events_json': json.dumps(events),
    })


def ical_feed(request):
    """Public iCal feed of booked dates."""
    from django.http import HttpResponse
    reservations = Reservation.objects.all()
    lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//26 Schoolhouse RT//EN',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
        'X-WR-CALNAME:26 Schoolhouse RT Availability',
    ]
    for r in reservations:
        lines += [
            'BEGIN:VEVENT',
            f'DTSTART;VALUE=DATE:{r.arrive_date.strftime("%Y%m%d")}',
            f'DTEND;VALUE=DATE:{r.leave_date.strftime("%Y%m%d")}',
            'SUMMARY:Reserved',
            f'UID:reservation-{r.pk}@schoolhouse',
            'END:VEVENT',
        ]
    lines.append('END:VCALENDAR')
    content = '\r\n'.join(lines)
    return HttpResponse(content, content_type='text/calendar')
