# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-04-24 18:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0020_auto_20190424_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='time_stamp',
            field=models.TimeField(auto_now_add=True, null=True, verbose_name='Time'),
        ),
    ]
