# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-05-12 23:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carga_horaria', '0011_asignacionextra_curso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignatura',
            name='base',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carga_horaria.AsignaturaBase'),
        ),
    ]
