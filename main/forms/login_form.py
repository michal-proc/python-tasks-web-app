from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'}))
