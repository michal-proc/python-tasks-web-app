# from django.contrib.auth.forms import UserCreationForm,
import django.forms as forms
from django.contrib.auth.forms import BaseUserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User


class RegisterForm(BaseUserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'}))
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'}))
    surname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'}))

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['surname']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
