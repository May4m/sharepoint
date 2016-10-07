
from django import forms


class RegisterForm(forms.Form):
    firstname = forms.CharField(label='first name')
    lastname = forms.CharField(label='last name')
    email = forms.EmailField()
    password = forms.CharField()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()