# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-24 03:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spell_bee', '0007_auto_20170523_1116'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quizinfo',
            options={'verbose_name': 'Spell Bee Quiz Info', 'verbose_name_plural': 'Spell Bee Quiz Info'},
        ),
        migrations.AlterModelOptions(
            name='spellbeequestion',
            options={'verbose_name': 'Spell Bee Question', 'verbose_name_plural': 'spell Bee Questions'},
        ),
    ]