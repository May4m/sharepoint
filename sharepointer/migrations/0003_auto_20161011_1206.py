# -*- coding: utf-8 -*-
# Generated by Django 1.11.dev20161011105145 on 2016-10-11 12:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0002_logentry_remove_auto_add'),
        ('sharepointer', '0002_auto_20161011_1133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileentity',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='user_ptr',
        ),
        migrations.DeleteModel(
            name='FileEntity',
        ),
        migrations.DeleteModel(
            name='UserModel',
        ),
    ]