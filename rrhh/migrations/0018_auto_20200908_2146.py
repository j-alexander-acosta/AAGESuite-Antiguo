# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-09-08 21:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0017_auto_20200902_2126'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Funcionario',
            new_name='Persona',
        ),
        migrations.AlterModelOptions(
            name='entrevista',
            options={'verbose_name': 'Entevista', 'verbose_name_plural': 'Entrevistas'},
        ),
        migrations.AlterModelOptions(
            name='persona',
            options={'verbose_name': 'Persona', 'verbose_name_plural': 'Personas'},
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='funcionario',
            new_name='persona',
        ),
        migrations.RemoveField(
            model_name='archivo',
            name='funcionario',
        ),
        migrations.RemoveField(
            model_name='entrevista',
            name='funcionario',
        ),
        migrations.AddField(
            model_name='archivo',
            name='contrato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.Contrato'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entrevista',
            name='contrato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.Contrato'),
            preserve_default=False,
        ),
    ]
