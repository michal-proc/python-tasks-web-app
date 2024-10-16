from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from ..controllers import auth_controller
from ..forms.login_form import LoginForm
from ..forms.register_form import RegisterForm
from django.contrib.auth import logout


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        return auth_controller.register(request)

    return render(request, 'main/register.html', {'form': form})


def login(request):
    form = LoginForm()
    if request.method == "POST":
        return auth_controller.login_user(request)

    return render(request, 'main/login.html', {'form': form})


def activate(request, uidb64, token):
    return auth_controller.activate(request, uidb64, token)


@require_http_methods(["POST"])
def logout_user(request):
    logout(request)
    return redirect('home')
