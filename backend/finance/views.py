from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import filter_transactions

from .forms import TransactionForm
from .models import Transaction

# Create your views here.
@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit = False)
            transaction.user = request.user
            transaction.save()
            return redirect("list_transactions")
    else:
        form = TransactionForm()

    return render(request, "finance/add_transaction.html", {"form" : form})


@login_required
def list_transactions(request):
    qs = Transaction.objects.filter(user = request.user).order_by('-date')
    transactions, type_filter, search_query, start_date, end_date = filter_transactions(request, qs)

    return render(request, 'finance/list_transactions.html', {'transactions' : transactions,
                                                              "search_query" : search_query,
                                                              "start_date" : start_date,
                                                              "end_date" : end_date,})
