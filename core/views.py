from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AppSettings
from .forms import AppSettingsForm


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
