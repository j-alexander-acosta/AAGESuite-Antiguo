# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-04-13 14:43
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carga_horaria', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='periodo',
            options={'verbose_name': 'Periodo', 'verbose_name_plural': 'Periodos'},
        ),
        migrations.AlterModelOptions(
            name='plan',
            options={'verbose_name': 'Plan', 'verbose_name_plural': 'Planes'},
        ),
        migrations.AlterField(
            model_name='plan',
            name='nivel',
            field=models.CharField(choices=[('PK', 'Pre kinder'), ('K', 'Kinder'), ('B1', 'Primero básico'), ('B2', 'Segundo básico'), ('B3', 'Tercero básico'), ('B4', 'Cuarto básico'), ('B5', 'Quinto básico'), ('B6', 'Sexto básico'), ('B7', 'Séptimo básico'), ('B8', 'Octavo básico'), ('M1', 'Primero medio'), ('M2', 'Segundo medio'), ('M3', 'Tercero medio'), ('M4', 'Cuarto medio')], max_length=8),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='horas',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(44)]),
        ),
    ]
