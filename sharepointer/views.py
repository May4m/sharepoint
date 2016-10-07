# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

# Create your views here.


def index(request):
    rendered = render_to_string("index.html")
    return render(request, "index.html", {})


def register(request):
    return HttpResponse("Registering user")

def login(request):
    return HttpResponse('logging in user')