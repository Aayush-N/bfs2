# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-04-23 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0017_auto_20190423_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teaches',
            name='active',
        ),
    ]
