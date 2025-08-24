from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, LoginForm, RegistrationForm, FeedbackForm
from .models import CustomUser


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

class RegisterView(CreateView):
    model = CustomUser
    form_class = RegistrationForm
    template_url = "accounts/register.html"
    success_url = reverse_lazy("login") # after registering, redirects to log in

@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html", { "user": request.user })

def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            print("Feedback sent") # replace with functionality
            return render(request, "accounts/feedbacksent.html") 
    else:
        form = FeedbackForm()

    return render(request, "accounts/feedback.html", { "form":form })
