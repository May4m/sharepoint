# -*- coding: utf-8 -*-
# Generated by Django 1.11.dev20161206060925 on 2016-12-06 06:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CentralFileStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=100, null=True)),
                ('file_content', models.TextField()),
                ('upload_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.BooleanField(default=False)),
                ('recipients', models.CharField(default='[]', max_length=900, null=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EditedFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_content', models.TextField()),
                ('edit_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=1000, null=True)),
                ('file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sharepointer.CentralFileStore')),
            ],
        ),
        migrations.CreateModel(
            name='SentFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sharepointer.CentralFileStore')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
