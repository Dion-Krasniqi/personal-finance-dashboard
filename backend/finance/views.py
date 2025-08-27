from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
    transactions = Transaction.objects.filter(user = request.user).order_by('-date')

    return render(request, 'finance/list_transactions.html', {'transactions' : transactions})
