# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-07-13 20:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carga_horaria', '0022_profesor_horas_no_aula'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsignacionNoAula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=255)),
                ('horas', models.DecimalField(decimal_places=1, max_digits=3)),
                ('curso', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carga_horaria.Periodo')),
                ('profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carga_horaria.Profesor')),
            ],
        ),
    ]
