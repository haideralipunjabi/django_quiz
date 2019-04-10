# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-14 03:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rapid_fire', '0002_auto_20170614_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rapidfirequestion',
            name='content',
            field=models.CharField(help_text='The question.', max_length=500, unique=True),
        ),
        migrations.AlterField(
            model_name='rapidfirequiz',
            name='timer',
            field=models.IntegerField(default=0, help_text='Time limit per rapid fire round.'),
        ),
    ]
