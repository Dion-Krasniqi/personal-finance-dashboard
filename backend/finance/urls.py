from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_transaction, name = 'add_transaction'),
    path('list/', views.list_transactions, name = 'list_transactions'),
    
    path('plaid/', views.plaid_link, name = 'plaid_link'),
    path('plaid/get_plaid_token/', views.get_plaid_token, name = 'get_plaid_token'),
    path('plaid/save_access_token/', views.save_access_token, name = 'save_access_token'),
    path('plaid/sync_transactions/', views.sync_transactions, name = 'sync_transactions'),

    path('', views.ReactDashboardView.as_view(), name='react-dashboard'),
]