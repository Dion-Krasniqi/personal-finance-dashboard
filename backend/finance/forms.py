from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount", "description", "type"] #handles user and date auto
        widgets = {
            "description" : forms.Textarea(attrs = {"rows" : 2, "cols" : 40}),
            "type" : forms.Select(attrs = {"class" : "form-control"}),
        }
