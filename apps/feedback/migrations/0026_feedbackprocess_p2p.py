# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-05-20 18:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0025_auto_20190520_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackprocess',
            name='p2p',
            field=models.BooleanField(default=False, verbose_name='Peer to peer'),
        ),
    ]
