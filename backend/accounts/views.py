from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from finance.models import Transaction
from finance.utils import filter_transactions
from django.db.models import Sum
from datetime import date

from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .forms import UserRegistrationForm, LoginForm, RegistrationForm, FeedbackForm, ProfileForm
from .models import CustomUser, Feedback



# Create your views here.

def home(request):
    return HttpResponse("Welcome to the Accounts App")

class UserRegistrationAPI_view(GenericAPIView):
    permission_classes = [AllowAny]

    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['tokens'] = {'refresh':str(token), 
                          'access': str(token.access_token),}
        return Response(data, status=status.HTTP_201_CREATED)


class UserLoginAPI_view(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = CustomUserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['tokens'] = {'refresh':str(token),
                          'access':str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)
    

class UserLogoutAPI_view(GenericAPIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserInfoAPI_view(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get_object(self):
        print('came')
        return self.request.user




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
            
        


