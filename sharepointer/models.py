# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FileEntity(models.Model):
    owner = models.ForeignKey(User)
    file = models.FileField(upload_to='/documents')
    upload_date = models.DateTimeField()