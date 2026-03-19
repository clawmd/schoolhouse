from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from reservations.models import Reservation
from .models import Month
from core.models import AppSettings


@login_required
def report(request):
    year = request.GET.get('year', str(timezone.now().year))
    try:
        year = int(year)
    except ValueError:
        year = timezone.now().year

    settings = AppSettings.get()
    tax_rate = float(settings.tax_rate)

    # Get all years that have reservations
    years = Reservation.objects.dates('arrive_date', 'year', order='DESC')
    year_list = [d.year for d in years]

    # Build monthly data
    months = []
    month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for m in range(1, 13):
        res = Reservation.objects.filter(
            payment_1_date__year=year, payment_1_date__month=m
        )
        res2 = Reservation.objects.filter(
            payment_2_date__year=year, payment_2_date__month=m
        )
        p1_total = res.aggregate(t=Sum('payment_1_actual'))['t'] or 0
        p2_total = res2.aggregate(t=Sum('payment_2_actual'))['t'] or 0
        total_revenue = float(p1_total) + float(p2_total)
        tax_due = round(total_revenue * tax_rate, 2)

        month_record, _ = Month.objects.get_or_create(year=year, month_number=m)

        months.append({
            'month_name': month_names[m - 1],
            'month_number': m,
            'p1_total': p1_total,
            'p2_total': p2_total,
            'total_revenue': total_revenue,
            'tax_due': tax_due,
            'record': month_record,
        })

    return render(request, 'reporting/report.html', {
        'months': months,
        'year': year,
        'year_list': year_list,
        'settings': settings,
    })
