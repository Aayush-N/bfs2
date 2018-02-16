# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-16 19:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('general', '0002_auto_20180216_1831'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('Excellent', 'Excellent'), ('Good', 'Good'), ('Satisfactory', 'Satisfactory'), ('Poor', 'Poor'), ('Very Poor', 'Very Poor')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Form Title')),
                ('description', models.CharField(max_length=250, verbose_name='Form Description')),
                ('student', models.BooleanField(default=False)),
                ('faculty', models.BooleanField(default=False)),
                ('hod', models.BooleanField(default=False)),
                ('vice_principal', models.BooleanField(default=False)),
                ('principal', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Question')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.FeedbackForm')),
            ],
        ),
        migrations.AddField(
            model_name='answers',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.Question'),
        ),
        migrations.AddField(
            model_name='answers',
            name='recipient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answers',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='general.Teaches'),
        ),
    ]
