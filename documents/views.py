from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reservations.models import Reservation
from .models import Document
from core.models import AppSettings


@login_required
def document_list(request):
    documents = Document.objects.all()
    return render(request, 'documents/list.html', {'documents': documents})


@login_required
def contract_print(request, reservation_id):
    res = get_object_or_404(Reservation, pk=reservation_id)
    settings = AppSettings.get()
    return render(request, 'documents/contract_print.html', {'res': res, 'settings': settings})


@login_required
def contract_print_ha(request, reservation_id):
    res = get_object_or_404(Reservation, pk=reservation_id)
    settings = AppSettings.get()
    return render(request, 'documents/contract_print_ha.html', {'res': res, 'settings': settings})


@login_required
def rules_print(request, reservation_id):
    res = get_object_or_404(Reservation, pk=reservation_id)
    settings = AppSettings.get()
    return render(request, 'documents/rules_print.html', {'res': res, 'settings': settings})


@login_required
def pet_rules_print(request, reservation_id):
    res = get_object_or_404(Reservation, pk=reservation_id)
    settings = AppSettings.get()
    return render(request, 'documents/pet_rules_print.html', {'res': res, 'settings': settings})


@login_required
def email_generator(request, reservation_id):
    res = get_object_or_404(Reservation, pk=reservation_id)
    settings = AppSettings.get()
    if request.method == 'POST':
        doc = Document(
            guest=res.guest,
            reservation_id=res.pk,
            email_recipient=request.POST.get('email_recipient', ''),
            email_subject=request.POST.get('email_subject', ''),
            email_body=request.POST.get('email_body', ''),
            created_by=request.user.username,
        )
        doc.save()
        messages.success(request, 'Email draft saved.')
        return redirect('reservations:detail', pk=res.pk)
    return render(request, 'documents/email_generator.html', {'res': res, 'settings': settings})
