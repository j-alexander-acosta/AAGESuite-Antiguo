# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-06-26 16:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0006_licencia_dias_habiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='licencia',
            name='fecha_retorno',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de retorno'),
        ),
        migrations.AddField(
            model_name='vacacion',
            name='fecha_retorno',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de retorno'),
        ),
    ]