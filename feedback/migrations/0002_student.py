# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-08 14:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.URLField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(max_length=64)),
                ('full_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='feedback',
            name='student',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='feedback.Student'),
            preserve_default=False,
        ),
    ]
