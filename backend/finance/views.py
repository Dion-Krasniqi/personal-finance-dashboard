from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators import csrf_excempt
from django.http import JsonResponse
from .utils import filter_transactions
from plaid import Client, environments
import os, json

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



PLAID_CLIENT_ID = os.environ.get('PLAID_CLIENT_ID')
PLAID_SECRET = os.environ.get('PLAID_SECRET')
client = Client(
    client_id = PLAID_CLIENT_ID,
    secret = PLAID_SECRET,
    environment = environments.Development, # could call it Sandbox or Prodcution
)

def get_plaid_token(request):
    try:
        link_token_request = {'user' : {'client_user_id' : str(request.user.id)},
                              'client_name' : 'Finance Board',
                              'products' : ['transactions'],
                              'country_codes' : ['US'],
                              'language' : 'en',
                              }
        response = client.link_token_create(link_token_request)
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({'error' : str(e)}, status = 500)

@csrf_excempt # just for the current setup
@login_required
def save_access_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            public_token = data.get('public_token') 
            exchange_response = client.item_public_token_exchange(public_token) # gives public key and recives perm access key
            request.user.access_token = exchange_response.get('access_token')
            request.user.item_id = exchange_response.get('item_id')
            request.user.save()
            return JsonResponse({'success':True},)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status = 500) 

    
    return JsonResponse({'error' : 'Invalid request method'}, status = 400)  
    