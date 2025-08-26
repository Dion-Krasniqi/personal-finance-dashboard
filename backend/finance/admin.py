from django.contrib import admin
from .models import Transaction

# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "amount", "date")
    list_filter = ("type", "date")
    search_fields = ("user-email", "description")
