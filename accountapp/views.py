from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginUserForm, RegisterUserForm


class LoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'accountapp/login.html'
    next_page = 'blogapp:home'


class RegistrationView(CreateView):
    form_class = RegisterUserForm
    template_name = 'accountapp/registration.html'
    success_url = reverse_lazy('accountapp:login')


class LogoutView(LogoutView):
    next_page = "/"
