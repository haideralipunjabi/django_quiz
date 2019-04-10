# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-14 03:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quiz_app', '0021_auto_20170613_0953'),
    ]

    operations = [
        migrations.CreateModel(
            name='RapidFireQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.IntegerField(help_text='Question number (relative to current quiz).')),
                ('content', models.CharField(help_text='The question.', max_length=500)),
            ],
            options={
                'verbose_name': 'rapid fire question',
                'verbose_name_plural': 'rapid fire questions',
            },
        ),
        migrations.CreateModel(
            name='RapidFireQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text="Quiz title e.g Math Storm!, Let's go Quantum!, The Hardest Quiz Ever!!!! etc.", max_length=50)),
                ('description', models.CharField(blank=True, help_text="Quiz description e.g 'A math quiz based on elementary school mathematics.'", max_length=200, null=True)),
                ('background_image', models.ImageField(blank=True, help_text='Background image for the quiz.', upload_to='')),
                ('max_questions', models.IntegerField(default=15, help_text='Maximum number of questions to be displayed in a single quiz sitting')),
                ('increment_per_question', models.IntegerField(default=4, help_text='The increment to be made in the score per right answer.')),
                ('negative_score', models.IntegerField(default=-1, help_text="The decrement to be made in the score per wrong answer (Include the minus '-' sign).")),
                ('timer', models.IntegerField(default=0, help_text='Time limit per question. Set 0 to disable timer.')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz_app.Team', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RapidFireScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz_app.Team')),
            ],
        ),
    ]
