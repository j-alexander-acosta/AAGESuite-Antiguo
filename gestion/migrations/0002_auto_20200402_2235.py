# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-04-02 22:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestion', '0001_initial'),
        ('recursos_humanos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundacion',
            name='asesores',
            field=models.ManyToManyField(related_name='_fundacion_asesores_+', to='recursos_humanos.FuncionarioFundacion'),
        ),
        migrations.AddField(
            model_name='fundacion',
            name='union',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.Union'),
        ),
        migrations.AddField(
            model_name='excelenciaacademica',
            name='colegio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.Colegio'),
        ),
        migrations.AddField(
            model_name='colegio',
            name='fundacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.Fundacion'),
        ),
    ]