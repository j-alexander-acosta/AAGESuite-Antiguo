# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-08-25 18:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carga_horaria', '0032_auto_20200813_2013'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asignatura',
            options={'ordering': ['base']},
        ),
        migrations.AddField(
            model_name='asistente',
            name='adventista',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profesor',
            name='adventista',
            field=models.BooleanField(default=False),
        ),
    ]