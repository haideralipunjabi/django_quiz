# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-22 05:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spell_bee', '0002_auto_20170522_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='spellbeequestion',
            name='meaning',
            field=models.CharField(default='', help_text='Meaning of the word.', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spellbeequestion',
            name='origin',
            field=models.CharField(blank=True, help_text='Origin of word. latic etc.', max_length=70, null=True),
        ),
        migrations.AddField(
            model_name='spellbeequestion',
            name='word_type',
            field=models.CharField(default=None, help_text='verb, noun, adjective etc.', max_length=50),
            preserve_default=False,
        ),
    ]
