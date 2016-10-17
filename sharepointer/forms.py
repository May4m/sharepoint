
from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class RegisterForm(forms.Form):
    firstname = forms.CharField(label='firstname')
    lastname = forms.CharField(label='lastname')
    email = forms.EmailField(label='email')
    password = forms.CharField(label='password')


class LoginForm(forms.Form):
    email = forms.EmailField(label='email')
    password = forms.CharField(label='password')


class ResetPasswordForm(forms.Form):
    email = forms.CharField(label=("email"), max_length=254)
