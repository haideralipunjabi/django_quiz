# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-22 05:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spell_bee', '0004_auto_20170522_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spellbeequestion',
            name='meaning',
            field=models.TextField(help_text='Meaning of the word.', max_length=500),
        ),
    ]