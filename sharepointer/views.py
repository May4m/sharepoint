# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import render, loader

from django.core.files.storage import FileSystemStorage

from django.views.generic import *

from forms import RegisterForm, LoginForm, ResetPasswordForm, UploadForm
import auth

import json
import dbgate
import models

# Create your views here.


def HttpJsonResponse(data):
    return HttpResponse(json.dumps(data))


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    return render(request, "index.html", {})


@login_required(login_url='/')
def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    sent = dbgate.get_all_sent_files(request.user)
    received = dbgate.get_all_received_files(request.user)
    edited = dbgate.get_all_edited_files();
    return render(request, 'home.html',
            {'username': request.user.first_name,
            'sent_files': sent,
            'received_files': received,
            'edited_files': edited,
            'no_of_files_sent': len(sent),
            'no_of_files_received': len(received),
            'no_of_files_edited': edited.count()
            })


class AuthCenter(object):

    @staticmethod
    def index(request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/home')
        return render(request, "index.html", {})

    @staticmethod
    def register(request):
        if request.user.is_authenticated:
            return render(request, "oops.html", {'error_code': 201, 'message': 'Someone has already logged in'})
        if request.method == 'POST':
            if request.user.is_authenticated:
                return render(request, "oops.html", {'error_code': 201, 'message': 'Someone has already logged in'})
            # create a form instance and populate it with data from the request:
            form = RegisterForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                get = form.cleaned_data.get
                if not auth.does_account_exist(get('email')):
                    user = auth.register_user(get('firstname'), get('lastname'), get('email'), get("password"))
                    messages.success(request, "A new user has been registered")
                    return render(request, 'info.html', {'message': 'An email has been sent to your account please verify it'})
                    #auth.login(request, user)
                    #return HttpResponseRedirect('/home')
                return render(request, 'oops.html', {'error_code': 100, 'message': 'account already exitst'})
            else:
                return HttpResponse('Invalid form submitted')
        return HttpResponseRedirect("/")

    @staticmethod
    def login(request):
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                if not auth.does_account_exist(email):
                    return render(request, "oops.html", {'error_code': 100, 'message': 'Account does not exist'})
                user = auth.authenticate_user(email, password)
                if user:
                    auth.login(request, user)
                    return HttpResponseRedirect('/home')
                return HttpResponse(json.dumps({'status': -200, 'message': 'authentication error'}))
            else:
                return HttpResponse('<h1>Invalid form submitted</h1<')
        return HttpResponseRedirect('/')

    @staticmethod
    def logout(request):
        if request.user.is_authenticated:
            auth.logout(request)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')

    @staticmethod
    def forgot_password(request):
        if request.user.is_authenticated:
            return HttpResponse('User already logged int')
        if request.method == 'GET':
            return render(request, "forgotpassword.html", {})
        elif request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                return AuthCenter.process_form(form, request)
            return HttpResponse('Invalid form')
        else:
            return HttpResponseServerError('Invalid method invoked %s' % request.method)

    @staticmethod
    def process_form(form, request):
        cred = form.cleaned_data.get('email')
        if not auth.does_account_exist(cred):
            return render(request, 'oops.html', {'error_code': 100, 'message': 'Account does not exist'})
        if auth.reset_password(request, cred):
            messages.success(request, 'An reset email has been sent to' + cred)
            return render(request, 'info.html', {'message': 'password reset email sent'})
        return render(request, 'oops.html', {'error_code': '500', 'message': 'could not send reset email'})

    @staticmethod
    def does_user_exist(request):
        first_check = User.objects.filter(email=request.GET['email']).exists()
        if first_check or auth.does_account_exist(request.GET['email']):
            return HttpResponse(json.dumps({'status': -1, 'message': 'Account already exitst'}))
        return HttpResponse(json.dumps({'status': 1, 'message': 'None'}))
    
    @staticmethod
    def validate_login(request):
        email = request.POST.get('email') or request.GET.get('email')
        password = request.POST.get('password') or request.GET.get('password')
        if request.user.is_authenticated:
            return HttpResponse(json.dumps({'status': -1, 'message': 'User already logged'}))
        if password == "" or email == "":
            return HttpResponse(json.dumps({'status': -1, 'message': 'Empty details entered'}))
        if auth.authenticate_user(email, password):
            return HttpResponse(json.dumps({'status': 1, 'message': 'successful'}))
        first_check = User.objects.filter(email=email).exists()
        if first_check:
            return HttpResponse(json.dumps({'status': -1, 'message': 'user not register'}))
        return HttpResponse(json.dumps({'status': -1, 'message': 'Please sign up first'}))

    @staticmethod
    def change_password(request):
        if request.user.is_authenticated:
            return render(request, "oops.html", {'error_code': 500, 'message': 'user already logged in'})
        if request.method == 'GET':
            token = request.GET.get('token')
            uid = request.GET.get('uid')
            pk = request.GET.get('pk')
            if not (token or uid or pk):
                return render(request, "oops.html", {'error_code': 500, 'message': 'An error occured'})
            user = User.objects.get(pk=pk)
            if user is None:
                return render(request, "oops.html", {'error_code': 500, 'message': 'we working on it'})
            return render(request, 'change_password_form.html', {'cid': str(user.pk)})
        elif request.method == "POST":
            password = request.POST.get('password')
            cid = request.POST.get('cid')
            user = User.objects.get(pk=cid)
            if not user:
                return render(request, 'oops.html', {'error_code': 500, 'message': 'invalid token'})
            user.set_password(password)
            user.save()
            return render(request, 'info.html', {'message': 'Your password has been changed'})
    
    @staticmethod
    def verify_account(request):
        email = request.GET.get('email')
        cid = request.GET.get('cid')
        if not (email or cid):
            return render(request, 'info.html', {'message': 'could not verify account'})
        user = User.objects.get(pk=cid)
        if not user:
            return render(request, 'info.html', {'message': 'could not verify account'})
        user.is_active = True
        user.save()
        if user:
            auth.login(request, user)
        return HttpResponseRedirect('/home')

    
class FileSharingCenter(object):

    @staticmethod
    @login_required(login_url='/')
    def send_file(request):
        if request.method == "GET":
            return render(request, "send_file_form.html", {'users': User.objects.all()})
        elif request.method == "POST":
            content = request.POST.get('content')
            filename = request.POST.get('filename')
            to = request.POST.get('to')
            file, _ = dbgate.upload_file(request.user, to, filename, content)
            dbgate.add_notification(file, "%s has sent a file to %s" % (request.user.first_name, to))
        return HttpResponse("form")

    @staticmethod
    @login_required(login_url='/')
    def delete_file(request):
        oid = request.GET.get('uid')
        section = request.GET.get('section')
        if oid and section:
            name = dbgate.delete_file(oid, section)
            dbgate.add_notification(None, "%s file has been deleted by %s" % (name, request.user.first_name))
            return HttpJsonResponse({"success": True})
        return HttpJsonResponse({"success": False})
    
    @staticmethod
    @login_required(login_url='/')
    def download_file(request):
        oid = request.GET.get('uid')
        section = request.GET.get('section')
        if oid is None or section is None:
            return HttpResponse("Could not download file")
        return dbgate.download_file(oid, section)

    @staticmethod
    @login_required(login_url='/')
    def edit_file(request):
        oid = request.GET.get('uid')
        section = request.GET.get('section')
        if section == "sent":
            obj = models.SentFiles.objects.get(pk=int(oid)).file
            file = obj.file_content
            uid = obj.pk
        elif section == "received":
            obj = models.CentralFileStore.objects.get(pk=int(oid))
            file = obj.file_content
            uid = obj.pk
        else:
            obj = models.EditedFiles.objects.get(pk=int(oid))
            file = obj.file_content
            uid = obj.pk
            dbgate.add_notification(None, "%s has viewed %s for editing" % (request.user.first_name, obj.file_name))
            return render(request, "edit_view.html", {'username': request.user.first_name, 'code': file, 'file_id': uid})
        dbgate.add_notification(None, "%s has viewed %s for editing" % (request.user.first_name, obj.file_name))
        return render(request, "edit.html", {'username': request.user.first_name, 'code': file, 'file_id': uid})

    @staticmethod
    @login_required(login_url='/')
    def update_file(request):
        uid = request.POST.get('uid')
        content = request.POST.get('content')
        if uid and content:
            dbgate.update_file(int(uid), str(content))
            return HttpResponse("{'success': true}")
        return HttpResponse("{'success': false}")

    @staticmethod
    @login_required(login_url='/')
    def get_file(request):
        uid = request.GET.get('uid')
        obj = models.CentralFileStore.objects.get(pk=int(uid))
        status = {'content': ''}
        if obj:
            status['content'] = obj.file_content
        return HttpJsonResponse(status)

    @staticmethod
    @login_required(login_url='/')
    def hard_edit(request):
        uid = request.POST.get('uid')
        content = request.POST.get('content')
        lobby = request.POST.get('lobby')
        if uid and content:
            dbgate.hard_file_update(int(uid), str(content), request.user, lobby)
            dbgate.add_notification(None, "%s has been edited by %s" % (obj.file_name, request.user.first_name))
            return HttpJsonResponse({'success': True})
        return HttpJsonResponse({'success': False})

    @staticmethod
    @login_required(login_url='/')
    def get_notifications(request):
        notifications = dbgate.read_notifications()
        return HttpJsonResponse({'any': dbgate.is_there_notifications(), 'notifications': notifications})