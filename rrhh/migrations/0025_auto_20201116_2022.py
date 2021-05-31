# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-11-16 20:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rrhh', '0024_auto_20201111_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='estadosolicitud',
            name='autor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='solicitudcontratacion',
            name='categoria',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Docente Directivo'), (2, 'Docente'), (3, 'Asistente de Educación'), (4, 'Otro Profesional')], default=2),
        ),
        migrations.AddField(
            model_name='solicitudcontratacion',
            name='tipo_contrato',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Indefinido'), (2, 'A plazo'), (3, 'Reemplazo')], default=1),
        ),
        migrations.AlterField(
            model_name='documentofuncionario',
            name='tipo_documento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rrhh.TipoDocumento'),
        ),
        migrations.AlterField(
            model_name='estadosolicitud',
            name='estado',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Aceptada'), (2, 'Pendiente'), (3, 'Rechazada'), (4, 'En espera de candidatos'), (5, 'Pendiente de aprobación'), (6, 'Aprobada')], default=2),
        ),
        migrations.AlterField(
            model_name='estadosolicitud',
            name='fecha',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='solicitudcontratacion',
            name='fecha_termino',
            field=models.DateField(blank=True, null=True),
        ),
    ]