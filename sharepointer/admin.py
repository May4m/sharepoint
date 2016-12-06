# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import CentralFileStore, SentFiles, EditedFiles, Notifications
# Register your models here.

admin.site.register([CentralFileStore, SentFiles, EditedFiles, Notifications])