from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, LoginForm, RegistrationForm, FeedbackForm
from .models import CustomUser, Feedback


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
            feedback = form.save(commit = False)
            feedback.user = request.user
            feedback.save()
            return render(request, "accounts/feedbacksent.html") 
    else:
        form = FeedbackForm()

    return render(request, "accounts/feedback.html", { "form":form })


@login_required
def feedback_list(request):
    if request.user.is_staff:
        feedbacks = Feedback.objects.all()
    else:
        feedbacks = Feedback.objects.filter(user = request.user)

    return render(request, "accounts/feedback_list.html", {"feedbacks" : feedbacks})

@login_required
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id = feedback_id)
    
    if feedback.user == request.user or request.user.is_staff:
        feedback.delete()
    
    return redirect("feedback_list")