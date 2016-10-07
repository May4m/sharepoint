# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from forms import RegisterForm, LoginForm
import auth

# Create your views here.

def index(request):
    return render(request, "index.html", {})


def register(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            get = form.cleaned_data.get
            if not auth.does_account_exist(get('email')):
                usr = auth.register_user(get('firstname'), get('lastname'),
                               get('email'), get("field_name"))
                
                return HttpResponse()
            return HttpResponse()
        else:
            return HttpResponse('<h1>Invalid form submitted</h1>')
    return HttpResponse('<h1>Invalid method for sensitive information')


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            usrname = form.cleaned_data.get('email').split('@')[0]
            password = form.cleaned_data.get('password').split('@')[0]
            user = auth.authenticate_user(usrname, password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect('/home?uid=' + get_user_id(user))
            return HttpResponse("{status: -200, message: 'authentication error''}")
        else:
            return HttpResponse('<h1>Invalid form submitted</h1<')
    return HttpResponseServerError('<h1>Invalid method for sensitive information')


def logout(request):
    auth.logout(request)


@login_required(login_url='/share/')
def home(request):
    if not request.user.is_authenticated:
        return HttpResponse('Welcome to the home Page')
    return HttpResponseRedirect('/share/')