from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from finance.models import Transaction
from django.db.models import Sum

from .forms import UserRegistrationForm, LoginForm, RegistrationForm, FeedbackForm, ProfileForm
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
    user = request.user

    transactions = Transaction.objects.filter(user = user).order_by('-date')

    filter_type = request.GET.get('type', 'all')
    if filter_type in ['income', 'expense']:
        transactions = transactions.filter(type = filter_type)

    month = request.GET.get('month')
    if month:
        try:
            year, month_num = map(int, month.split('-'))
            transactions = transactions.filter(date__year = year, date__month = month_num)
        except ValueError:
            pass
        

    income = transactions.filter(type = 'income').aggregate(total = Sum('amount'))['total'] or 0 # if there isnt any, it doesnt return None but 0
    expenses = transactions.filter(type = 'expense').aggregate(total = Sum('amount'))['total'] or 0
    balance = income - expenses

    return render(request, "accounts/dashboard.html", { "transactions" : transactions,
                                                        "income" : income,
                                                        "expenses" : expenses,
                                                        "balance" : balance,
                                                        "filter_type" : filter_type,
                                                        "month" : month,
                                                    })


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

@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        form = ProfileForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile update successfully")
            return redirect("profile")
    else:
            form = ProfileForm(instance = user)

    return render(request, "accounts/profile.html", {"form" : form})