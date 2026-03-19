from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Expense
from .forms import ExpenseForm
from core.models import AppSettings


@login_required
def expense_list(request):
    expenses = Expense.objects.all()
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    if q:
        expenses = expenses.filter(Q(title__icontains=q) | Q(note__icontains=q))
    if category:
        expenses = expenses.filter(tax_category=category)
    settings = AppSettings.get()
    return render(request, 'expenses/list.html', {
        'expenses': expenses, 'q': q, 'category': category, 'settings': settings,
        'categories': Expense.TAX_CATEGORY_CHOICES,
    })


@login_required
def expense_new(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense added.')
            return redirect('expenses:list')
    else:
        form = ExpenseForm()
    settings = AppSettings.get()
    return render(request, 'expenses/form.html', {'form': form, 'title': 'New Expense', 'settings': settings})


@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated.')
            return redirect('expenses:list')
    else:
        form = ExpenseForm(instance=expense)
    settings = AppSettings.get()
    return render(request, 'expenses/form.html', {'form': form, 'expense': expense, 'title': 'Edit Expense', 'settings': settings})


@login_required
def expense_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('expenses:list')
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted.')
        return redirect('expenses:list')
    return render(request, 'expenses/confirm_delete.html', {'expense': expense})
