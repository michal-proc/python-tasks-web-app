from django import forms
from django.contrib.auth.models import User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
