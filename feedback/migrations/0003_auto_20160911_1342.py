# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-11 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_auto_20160911_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='html_url',
            field=models.CharField(default='#', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exercise',
            name='html_url',
            field=models.CharField(default='#', max_length=255),
            preserve_default=False,
        ),
    ]
