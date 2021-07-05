# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-11-26 21:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0027_auto_20201124_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudcontratacion',
            name='reemplazando_licencia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rrhh.LicenciaFuncionarioColegio', verbose_name='En reemplazo de'),
        ),
        migrations.AlterField(
            model_name='documentofuncionario',
            name='tipo_documento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rrhh.TipoDocumento'),
        ),
        migrations.AlterField(
            model_name='solicitudrenovacion',
            name='estado',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Pendiente'), (2, 'Aceptada'), (3, 'Rechazada'), (4, 'Aceptada y contratado')], default=1),
        ),
    ]
