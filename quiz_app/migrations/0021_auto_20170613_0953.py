# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-13 04:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0020_auto_20170613_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='score',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='score',
            name='team',
        ),
        migrations.AlterModelOptions(
            name='quiz',
            options={'verbose_name': 'Quiz', 'verbose_name_plural': 'Quizzes'},
        ),
        migrations.DeleteModel(
            name='Score',
        ),
        migrations.AddField(
            model_name='quizscore',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz_app.Quiz'),
        ),
        migrations.AddField(
            model_name='quizscore',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz_app.Team'),
        ),
    ]
