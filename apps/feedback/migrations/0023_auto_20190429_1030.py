# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-04-29 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0022_studentconsolidatedreport_process'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedbackprocess',
            name='year',
        ),
        migrations.AddField(
            model_name='feedbackprocess',
            name='date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Date'),
        ),
    ]
