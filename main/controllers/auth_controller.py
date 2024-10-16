from django.contrib import messages
from django.utils.encoding import force_str
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode

from mail.sender import send_activation_email
from main.forms.login_form import LoginForm
from main.forms.register_form import RegisterForm


def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        send_activation_email(request, user)

        messages.info(request, 'Check your email to activate your account')
        return redirect('home')
    else:
        messages.error(request, 'Invalid data provided. Please try again')
        return redirect('register')


def login_user(request):
    form = LoginForm(request.POST)

    if not form.is_valid():
        messages.error(request, 'Invalid credentials')
        return redirect('login')

    username_or_email = form.cleaned_data['username']
    password = form.cleaned_data['password']

    user = authenticate(request, username=username_or_email, password=password)

    # Login via e-mail
    if user is None:
        user_queryset = User.objects.filter(email=username_or_email)
        if user_queryset.exists():
            user_obj = user_queryset.first()
            user = authenticate(request, username=user_obj.username, password=password)

    if user is None:
        messages.error(request, 'Invalid credentials')
        return redirect('login')

    if user.is_active:
        login(request, user)
        return redirect('home')

    messages.error(request, 'Inactive account')
    return redirect('login')


def activate(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.info(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('home')

    messages.error(request, 'Cannot activate your account')
    return redirect('home')
