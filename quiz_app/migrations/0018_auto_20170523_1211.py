# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-23 06:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('quiz_app', '0017_layoutassets_team_intro_background'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='quiz',
        ),
        migrations.AddField(
            model_name='score',
            name='content_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='score',
            name='object_id',
            field=models.PositiveIntegerField(default=2),
            preserve_default=False,
        ),
    ]
