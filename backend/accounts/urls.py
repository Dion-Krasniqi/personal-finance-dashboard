from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path("register/", views.RegisterView.as_view(template_name = "accounts/register.html"), name="register"),
    path("login/", views.CustomLoginView.as_view(template_name = "accounts/login.html"), name="login"),
    path("logout/", views.CustomLogoutView.as_view(next_page = "login"), name="logout"),
]