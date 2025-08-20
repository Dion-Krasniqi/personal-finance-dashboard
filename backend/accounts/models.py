from django.db import models
from django.contrib.auth.models import AbstractUser #django default model




# Models

class CustomUser(AbstractUser):
    # These are extra fields we're adding
    email = models.EmailField(unique=True) # Make email unique
    # Custom field we've added
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.username
