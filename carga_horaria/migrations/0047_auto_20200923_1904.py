# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-09-23 19:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carga_horaria', '0046_remove_asignatura_periodo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignatura',
            name='perioda',
            field=models.ManyToManyField(to='carga_horaria.Periodo'),
        ),
    ]
