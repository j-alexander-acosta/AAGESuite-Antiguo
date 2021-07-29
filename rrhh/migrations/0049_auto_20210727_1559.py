# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2021-07-27 19:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0048_auto_20210726_1655'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Ciudad',
                'verbose_name_plural': 'Ciudades',
            },
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Comuna',
                'verbose_name_plural': 'Comunas',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('numero', models.PositiveSmallIntegerField(default=0)),
                ('numero_romano', models.CharField(blank=True, max_length=5, null=True)),
            ],
            options={
                'verbose_name': 'Región',
                'verbose_name_plural': 'Regiones',
                'ordering': ['numero'],
            },
        ),
        migrations.AlterField(
            model_name='colegio',
            name='estado',
            field=models.CharField(choices=[('particular_subvencionado', 'Particular Subvencionado'), ('gratuito', 'Gratuito'), ('particular', 'Particular')], default='particular_subvencionado', max_length=25),
        ),
        migrations.AlterField(
            model_name='documentofuncionario',
            name='tipo_documento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rrhh.TipoDocumento'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='ciudad',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='comuna',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='estado_civil',
            field=models.CharField(choices=[('soltero', 'SOLTERO'), ('casado', 'CASADO'), ('divorsiado', 'DIVORSIADO'), ('viudo', 'VIUDO')], default='soltero', max_length=100),
        ),
        migrations.AlterField(
            model_name='persona',
            name='genero',
            field=models.CharField(choices=[('femenino', 'FEMENINO'), ('masculino', 'MASCULINO')], default='masculino', max_length=100, verbose_name='Género'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='nacionalidad',
            field=models.CharField(choices=[('chilena', 'CHILENA'), ('extranjera', 'EXTRANJERA')], default='chilena', max_length=100),
        ),
        migrations.AlterField(
            model_name='persona',
            name='profesion',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Título profesional'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='religion',
            field=models.BooleanField(default=True, verbose_name='Religión'),
        ),
        migrations.AddField(
            model_name='comuna',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.Region', verbose_name='Región'),
        ),
        migrations.AddField(
            model_name='ciudad',
            name='comuna',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.Comuna'),
        ),
    ]