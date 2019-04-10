# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-14 04:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rapid_fire', '0003_auto_20170614_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rapidfirequestion',
            name='question_number',
            field=models.IntegerField(help_text='Question number (relative to current quiz).', unique=True),
        ),
    ]