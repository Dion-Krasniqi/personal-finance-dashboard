from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView

from .forms import UserRegistrationForm, LoginForm


# Create your views here.

def home(request):
    return HttpResponse("Welcome to the Accounts App")

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", { "form":form })    


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm

class CustomLogoutView(LogoutView):
    next_page = "/"