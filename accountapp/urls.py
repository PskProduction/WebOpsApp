from django.urls import path

from .views import LoginView, LogoutView, RegistrationView

app_name = "accountapp"

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
