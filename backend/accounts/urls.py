from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path("register/", views.RegisterView.as_view(template_name = "accounts/register.html"), name="register"),
    path("login/", views.CustomLoginView.as_view(template_name = "accounts/login.html"), name="login"),
    path("logout/", views.CustomLogoutView.as_view(next_page = "login"), name="logout"),
    path("dashboard/", views.dashboard, name = "dashboard"),
    path("feedback/", views.feedback_view, name = "feedback"),
    path("feedback/list", views.feedback_list, name = "feedback_list"),
    path("feedback/delete/<int:feedback_id>/", views.delete_feedback, name = "delete_feedback"),
    path("profile/", views.profile_view, name = "profile"),
    
]