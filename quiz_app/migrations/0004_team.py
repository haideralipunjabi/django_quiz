# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-08 04:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0003_layoutassets_intro_background_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Team name', max_length=70)),
                ('description', models.CharField(help_text='Team description', max_length=500)),
                ('photo', models.ImageField(help_text='Intro image for the team.', upload_to='')),
            ],
        ),
    ]