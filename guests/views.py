from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Guest
from .forms import GuestForm


@login_required
def guest_list(request):
    q = request.GET.get('q', '')
    guests = Guest.objects.all()
    if q:
        guests = guests.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(email__icontains=q) |
            Q(city__icontains=q)
        )
    return render(request, 'guests/list.html', {'guests': guests, 'q': q})


@login_required
def guest_detail(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    reservations = guest.reservation_set.order_by('-arrive_date')
    return render(request, 'guests/detail.html', {
        'guest': guest,
        'reservations': reservations,
    })


@login_required
def guest_new(request):
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            guest = form.save()
            messages.success(request, f'Guest {guest} added.')
            return redirect('guests:detail', pk=guest.pk)
    else:
        form = GuestForm()
    return render(request, 'guests/form.html', {'form': form, 'title': 'New Guest'})


@login_required
def guest_edit(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    if request.method == 'POST':
        form = GuestForm(request.POST, instance=guest)
        if form.is_valid():
            form.save()
            messages.success(request, f'Guest {guest} updated.')
            return redirect('guests:detail', pk=guest.pk)
    else:
        form = GuestForm(instance=guest)
    return render(request, 'guests/form.html', {'form': form, 'guest': guest, 'title': 'Edit Guest'})


@login_required
def guest_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('guests:list')
    guest = get_object_or_404(Guest, pk=pk)
    if request.method == 'POST':
        name = str(guest)
        guest.delete()
        messages.success(request, f'Guest {name} deleted.')
        return redirect('guests:list')
    return render(request, 'guests/confirm_delete.html', {'guest': guest})


@login_required
def guest_search_htmx(request):
    """HTMX endpoint: returns guest dropdown options."""
    q = request.GET.get('q', '')
    guests = []
    if q:
        guests = Guest.objects.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q)
        )[:10]
    return render(request, 'guests/htmx_search_results.html', {'guests': guests})
