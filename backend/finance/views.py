from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import filter_transactions
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.exceptions import ApiException
import os, json, logging

from .forms import TransactionForm
from .models import Transaction, PlaidCredentials

logger = logging.getLogger(__name__)
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


# plaid setup
PLAID_CLIENT_ID = os.environ.get('PLAID_CLIENT_ID')
PLAID_SECRET = os.environ.get('PLAID_SECRET')
configuration = plaid.Configuration(
    host = plaid.Environment.Sandbox,
    api_key = {
        'clientID' : PLAID_CLIENT_ID,
        'secret' : PLAID_SECRET,
        'plaid-version' : '2025-08-13'
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

@login_required
def get_plaid_token(request):
    try:
        link_token_request = LinkTokenCreateRequest(
            products = [Products("transactions")],
            client_name = "FinBoard",
            country_codes = [CountryCode["US"]],
            language = 'en',
            user = LinkTokenCreateRequestUser(client_user_id = str(request.user.id))
        )
        response = client.link_token_create(link_token_request)
        return JsonResponse(response.to_dict())
    except ApiException as e:
        logger.error(f"Plaid Api Exception: {e}")
        return JsonResponse({'error' : json.loads(e.body)}, status = e.status)
    except Exception as e:
        logger.error(f"An unexpected error occured: {e}")
        return JsonResponse({'error' : str(e)}, status = 500)

@csrf_exempt # just for the current setup
@login_required
def save_access_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            public_token = data.get('public_token') 

            exchange_request = ItemPublicTokenExchangeRequest(public_token = public_token)
            exchange_response = client.item_public_token_exchange(exchange_request) # gives public key and recives perm access key
           
            access_token = exchange_response.get('access_token')
            item_id = exchange_response.get('item_id')
            
            PlaidCredentials.objects.update_or_create(
                user = request.user,
                defaults ={'access_token' : access_token, 'item_id' : item_id}
            )
            return JsonResponse({'success':True},)
        except ApiException as e:
            logger.error(f"Plaid Api Exception: {e}")
            return JsonResponse({'error' : json.loads(e.body)}, status = e.status)
        except Exception as e:
            logger.error(f"An unexpected error occured: {e}")
            return JsonResponse({'error' : str(e)}, status = 500) 

    
    return JsonResponse({'error' : 'Invalid request method'}, status = 400)  



    