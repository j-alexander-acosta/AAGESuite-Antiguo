# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-08-03 21:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0010_remove_contrato_horas'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='horas',
            field=models.PositiveIntegerField(default=1, verbose_name='Horas contratadas'),
            preserve_default=False,
        ),
    ]