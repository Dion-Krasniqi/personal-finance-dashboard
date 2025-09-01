from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_transaction, name = 'add_transaction'),
    path('list/', views.list_transactions, name = 'list_transactions'),
    path('get-plaid-token/', views.get_plaid_token, name = 'get_plaid_token'),
    path('save-access-token/', views.save_access_token, name = 'save-access-token'),
]