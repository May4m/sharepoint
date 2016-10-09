# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import render, loader

from django.views.generic import *

from forms import RegisterForm, LoginForm, ResetPasswordForm
import auth

import json


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    return render(request, "index.html", {})


@login_required(login_url='/')
def home(request):
    if request.user.is_authenticated:
        return HttpResponse('Welcome to the home Page %s' % request.user.email)
    return HttpResponseRedirect('/')


class AuthCenter(object):

    @staticmethod
    def index(request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/home')
        return render(request, "index.html", {})

    @staticmethod
    def register(request):
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = RegisterForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                get = form.cleaned_data.get
                if not auth.does_account_exist(get('email')):
                    auth.register_user(get('firstname'), get('lastname'), get('email'), get("password"))
                    return HttpResponse('user succesfully registered')
                return HttpResponse('User already registered' + get('username'))
            else:
                return HttpResponse('Invalid form submitted')
        return HttpResponse('Invalid method for sensitive information')

    @staticmethod
    def login(request):
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                print email, password
                user = auth.authenticate_user(email, password)
                if user:
                    auth.login(request, user)
                    return HttpResponse('User successfuly logged in')
                return HttpResponse("{status: -200, message: 'authentication error''}")
            else:
                return HttpResponse('<h1>Invalid form submitted</h1<')
        return HttpResponseServerError('<h1>Invalid method for sensitive information')

    @staticmethod
    def logout(request):
        if request.user.is_authenticated:
            auth.logout(request)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')

    @staticmethod
    def forgot_password(request):
        if request.method == 'GET':
            return render(request, "forgotpassword.html", {})
        elif request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                ForgotPasswordRequest.process_form(form, request)
            return HttpResponse('Invalid form')
        else:
            return HttpResponseServerError('Invalid method invoked %s' % request.method)

    @staticmethod
    def process_form(form, request):
        cred = form.cleaned_data.get('email')
        if auth.reset_password(request, cred):
            result = form.form_valid(form)
            messages.success(request, 'An email has been sent to ' + data + ". Please check its inbox to continue reseting password.")
        else:
            result = form.form_invalid(form)
            messages.error(request, 'No user is associated with this email address')
        return result

    @staticmethod
    def does_user_exist(request):
        if auth.does_account_exist(request.GET['email']):
            return HttpResponse(json.dumps({'status': -1, 'message': 'Account already exitst'}))
        return HttpResponse(json.dumps({'status': 1, 'message': 'None'}))