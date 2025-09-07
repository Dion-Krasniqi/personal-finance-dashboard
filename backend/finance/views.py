from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import TemplateView
from .utils import filter_transactions
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.exceptions import ApiException
from plaid.model.transactions_sync_request import TransactionsSyncRequest
import os, json, logging
from dotenv import load_dotenv

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
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
configuration = plaid.Configuration(
    host = plaid.Environment.Sandbox,
    api_key = {
        'clientId' : PLAID_CLIENT_ID,
        'secret' : PLAID_SECRET,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

@csrf_exempt
@login_required
def get_plaid_token(request):
    user_id = str(request.user.id)
    link_token_request = LinkTokenCreateRequest(
            user = LinkTokenCreateRequestUser(client_user_id = user_id),
            products = [Products("transactions")],
            client_name = "FinBoard",
            country_codes = [CountryCode("US")],
            language = 'en',
            
        )
    try:
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
                defaults = {'access_token' : access_token, 'item_id' : item_id}
            )
            return JsonResponse({'success':True},)
        except ApiException as e:
            logger.error(f"Plaid Api Exception: {e}")
            return JsonResponse({'error' : json.loads(e.body)}, status = e.status)
        except Exception as e:
            logger.error(f"An unexpected error occured: {e}")
            return JsonResponse({'error' : str(e)}, status = 500) 

    
    return JsonResponse({'error' : 'Invalid request method'}, status = 400)  

def plaid_link(request):
    return render(request, 'finance/plaid_link.html')

def sync_transactions(request):
    try:
     plaid_creds = PlaidCredentials.objects.get(user=request.user)
     access_token = plaid_creds.access_token
     
     sync_request = TransactionsSyncRequest(access_token = access_token)
     response = client.transactions_sync(sync_request)
     transactions = response['added']

     for transaction in transactions:
         amount = abs(transaction['amount'])
         transaction_type = 'income' if transaction['amount']<0 else 'expense'

         Transaction.objects.update_or_create(
             transaction_id = transaction['transaction_id'],
             defaults = {
                 'user' : request.user,
                 'amount' : amount,
                 'type' : transaction_type,
                 'description' : transaction['merchant_name'] or transaction['name'],
                 'date' : transaction['date'],
             }
         )
     return JsonResponse({'success': True, 'synced_count':len(transactions)})
    except PlaidCredentials.DoesNotExist:
        return JsonResponse({'error':'User has no Plaid credentials'}, status = 400)


    
class ReactDashboardView(TemplateView):
    template_name = 'finance/index.html'

def get_sample_data(TemplateView):
    sample_data = {
        'message':'Hello',
        'data':[
            {'id':1,'name':'Item A'},
            {'id':2,'name':'Item B'},
        ]
    }
    return JsonResponse(sample_data)

@csrf_exempt
@login_required
def create_transaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            transaction = Transaction.objects.create(user=request.user,
                                                     description = data['description'],
                                                     amount=data['amount'],
                                                     type=data['type'])
            return JsonResponse({"message":"Transaction created", 'id':transaction.transaction_id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error":"Invalid JSON format"}, status=400)
        except KeyError as e:
            return JsonResponse({"error":f'Missing key: {e}'},status=400)

    return JsonResponse({"error":"Invalid request method"}, status=405)

@csrf_exempt
@login_required
def delete_transaction(request, transaction_id):
    if request.method == 'DELETE':
        try: 
            transaction = Transaction.objects.filter(id=transaction_id, user=request.user)
            transaction.delete()
            return JsonResponse({"message":"Transaction deleted successfully."}, status=200)
        except Transaction.DoesNotExist:
            return JsonResponse({"erros":"Transaction not found."}, status=404)
    return JsonResponse({"error":"Invalid request method."}, status=405)
