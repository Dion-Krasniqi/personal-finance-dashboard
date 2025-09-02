from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager # django default modelS
from django.conf import settings




# Models

class CustomeUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # this is for hashing the password
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):


        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

# class CustomUser(AbstractBaseUser, PermissionsMixin):
    # These are extra fields we're adding
#    email = models.EmailField(unique=True) # Make email unique
    # Custom field we've added
#    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

#    def __str__(self):
#        return self.username

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    #access_token = models.CharField(max_length=100, null=True)
    #item_id = models.CharField(max_length=100,null=True)

    objects = CustomeUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Feedback from {self.user.email} at {self.created_at}. Message: {self.message}"

