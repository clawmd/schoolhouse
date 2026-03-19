from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Issue
from .forms import IssueForm


@login_required
def issue_list(request):
    show = request.GET.get('show', 'open')
    issues = Issue.objects.all()
    if show == 'open':
        issues = issues.filter(completion_date__isnull=True)
    elif show == 'closed':
        issues = issues.filter(completion_date__isnull=False)
    return render(request, 'issues/list.html', {'issues': issues, 'show': show})


@login_required
def issue_new(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.created_by = request.user
            issue.save()
            messages.success(request, 'Issue logged.')
            return redirect('issues:list')
    else:
        form = IssueForm()
    return render(request, 'issues/form.html', {'form': form, 'title': 'New Issue'})


@login_required
def issue_edit(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            messages.success(request, 'Issue updated.')
            return redirect('issues:list')
    else:
        form = IssueForm(instance=issue)
    return render(request, 'issues/form.html', {'form': form, 'issue': issue, 'title': 'Edit Issue'})


@login_required
def issue_complete(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    issue.completion_date = timezone.now().date()
    issue.save()
    messages.success(request, f'"{issue.title}" marked complete.')
    return redirect('issues:list')


@login_required
def issue_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('issues:list')
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == 'POST':
        issue.delete()
        messages.success(request, 'Issue deleted.')
        return redirect('issues:list')
    return render(request, 'issues/confirm_delete.html', {'issue': issue})
