# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class FileEntity(models.Model):
    file = models.FileField(upload_to='/uploads')
    date_uploaded = models.DateTimeField(auto_now_add=True)