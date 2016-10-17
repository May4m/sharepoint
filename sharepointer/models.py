# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage


# Create your models here.
import os

class FileModel(models.Model):
    file = models.FileField()
    date_uploaded = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0, editable=False)
    owner = models.ForeignKey(User)

class SentFile(FileModel):
    pass


class ReceivedFile(FileModel):
    pass