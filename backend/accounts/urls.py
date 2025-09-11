from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.UserRegistrationAPI_view.as_view(), name='register-user'),
    path('login/', views.UserLoginAPI_view.as_view(), name='login-user'),
    path('logout/', views.UserLogoutAPI_view.as_view(), name='logout-user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),



    #path("register/", views.RegisterView.as_view(template_name = "accounts/register.html"), name="register"),
    #path("login/", views.CustomLoginView.as_view(template_name = "accounts/login.html"), name="login"),
    #path("logout/", views.CustomLogoutView.as_view(next_page = "login"), name="logout"),
    
    path("feedback/", views.feedback_view, name = "feedback"),
    path("feedback/list", views.feedback_list, name = "feedback_list"),
    path("feedback/delete/<int:feedback_id>/", views.delete_feedback, name = "delete_feedback"),
    path("profile/", views.profile_view, name = "profile"),
    
   
]