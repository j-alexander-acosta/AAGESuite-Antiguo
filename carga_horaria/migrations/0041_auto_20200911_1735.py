# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-09-11 17:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carga_horaria', '0040_auto_20200911_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistente',
            name='rut',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AddField(
            model_name='profesor',
            name='rut',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
