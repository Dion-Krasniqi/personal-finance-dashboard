from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import UserRegistrationForm, CustomUserChangeForm

# Register your models here.
@admin.register
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = UserRegistrationForm
    form =  CustomUserChangeForm
    search_fields = ("email",)
    ordering = ("email",)

