from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import MaintenanceTask
from .forms import MaintenanceTaskForm


@login_required
def task_list(request):
    show = request.GET.get('show', 'open')
    tasks = MaintenanceTask.objects.all()
    if show == 'open':
        tasks = tasks.filter(status='To Do')
    elif show == 'done':
        tasks = tasks.filter(status='Done')
    return render(request, 'maintenance/list.html', {'tasks': tasks, 'show': show})


@login_required
def task_new(request):
    if request.method == 'POST':
        form = MaintenanceTaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task added.')
            return redirect('maintenance:list')
    else:
        form = MaintenanceTaskForm()
    return render(request, 'maintenance/form.html', {'form': form, 'title': 'New Maintenance Task'})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(MaintenanceTask, pk=pk)
    if request.method == 'POST':
        form = MaintenanceTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated.')
            return redirect('maintenance:list')
    else:
        form = MaintenanceTaskForm(instance=task)
    return render(request, 'maintenance/form.html', {'form': form, 'task': task, 'title': 'Edit Task'})


@login_required
def task_complete(request, pk):
    task = get_object_or_404(MaintenanceTask, pk=pk)
    task.status = 'Done'
    task.completed_date = timezone.now().date()
    task.save()
    messages.success(request, f'"{task.title}" marked complete.')
    return redirect('maintenance:list')


@login_required
def task_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('maintenance:list')
    task = get_object_or_404(MaintenanceTask, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted.')
        return redirect('maintenance:list')
    return render(request, 'maintenance/confirm_delete.html', {'task': task})
