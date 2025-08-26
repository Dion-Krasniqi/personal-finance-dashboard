from django.db import models
from django.conf import settings

# Create your models here.

class Transaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE, #links to custom user from accounts app
        related_name = "transactions",
    )
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    description = models.CharField(max_length = 255, blank = True)
    date = models.DateTimeField(auto_now_add = True)
    type = models.CharField(
        max_length = 10,
        choices = [("income", "Income"), ("expense", "Expense")]
    )

    def __str__(self):
        return f"{self.user.email} - {self.type} : {self.amount}"
