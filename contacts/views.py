from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Contact
from .forms import ContactForm


@login_required
def contact_list(request):
    q = request.GET.get('q', '')
    contacts = Contact.objects.all()
    if q:
        contacts = contacts.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(company__icontains=q) | Q(service_type__icontains=q)
        )
    return render(request, 'contacts/list.html', {'contacts': contacts, 'q': q})


@login_required
def contact_new(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, f'Contact {contact} added.')
            return redirect('contacts:list')
    else:
        form = ContactForm()
    return render(request, 'contacts/form.html', {'form': form, 'title': 'New Contact'})


@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, f'Contact {contact} updated.')
            return redirect('contacts:list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/form.html', {'form': form, 'contact': contact, 'title': 'Edit Contact'})


@login_required
def contact_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('contacts:list')
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact deleted.')
        return redirect('contacts:list')
    return render(request, 'contacts/confirm_delete.html', {'contact': contact})
