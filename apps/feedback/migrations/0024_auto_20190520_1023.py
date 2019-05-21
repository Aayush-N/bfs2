# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-05-20 10:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feedback', '0023_auto_20190429_1030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consolidatedreport',
            name='department',
        ),
        migrations.RemoveField(
            model_name='consolidatedreport',
            name='name',
        ),
        migrations.RemoveField(
            model_name='studentconsolidatedreport',
            name='name',
        ),
        migrations.AddField(
            model_name='consolidatedreport',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='studentconsolidatedreport',
            name='batch',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name="Student's Batch"),
        ),
        migrations.AddField(
            model_name='studentconsolidatedreport',
            name='sec',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name="Student's Section"),
        ),
        migrations.AddField(
            model_name='studentconsolidatedreport',
            name='sem',
            field=models.IntegerField(blank=True, max_length=10, null=True, verbose_name="Student's Semester"),
        ),
        migrations.AddField(
            model_name='studentconsolidatedreport',
            name='sub_batch',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name="Student's sub batch"),
        ),
        migrations.AddField(
            model_name='studentconsolidatedreport',
            name='subject',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name="Student's subject"),
        ),
        migrations.AddField(
            model_name='studentconsolidatedreport',
            name='ug',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='studentconsolidatedreport',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='studentconsolidatedreport',
            name='total',
            field=models.FloatField(blank=True, max_length=10, null=True, verbose_name='Total value they got'),
        ),
    ]
