from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout

from mail.sender import send_activation_email
from ..forms import UserUpdateForm, EmailUpdateForm
from django.views.decorators.http import require_http_methods


@login_required
def account_settings(request):
    user = request.user
    form = UserUpdateForm(instance=user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your profile has been updated successfully.')
            return redirect('account_settings')

    return render(request, 'panel/account_settings.html', {'form': form, 'user': user})


@login_required
@require_http_methods(["POST"])
def update_email(request):
    user = request.user
    form = EmailUpdateForm(request.POST, instance=user)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        send_activation_email(request, user)

        messages.info(request, 'Check your email to reactivate your account.')
        logout(request)
        return redirect('home')
    else:
        messages.error(request, 'Please correct the error below.')

    return redirect('account_settings')


@login_required
@require_http_methods(["POST"])
def update_password(request):
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.info(request, 'Your password was successfully updated!')
    else:
        messages.error(request, 'Please correct the error below.')
    return redirect('account_settings')
