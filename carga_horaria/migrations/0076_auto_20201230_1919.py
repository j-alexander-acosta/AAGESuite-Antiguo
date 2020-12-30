# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-12-30 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carga_horaria', '0075_auto_20201217_0136'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistente',
            name='tipo',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Indefinido'), (2, 'Plazo fijo'), (3, 'Reemplazo')], default=1, verbose_name='Tipo de contrato'),
        ),
        migrations.AddField(
            model_name='historicalasistente',
            name='tipo',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Indefinido'), (2, 'Plazo fijo'), (3, 'Reemplazo')], default=1, verbose_name='Tipo de contrato'),
        ),
    ]