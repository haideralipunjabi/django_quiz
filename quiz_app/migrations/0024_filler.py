# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-29 05:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0023_auto_20170622_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Title of the video', max_length=50)),
                ('video', models.FileField(help_text='The filler video', upload_to='')),
            ],
        ),
    ]