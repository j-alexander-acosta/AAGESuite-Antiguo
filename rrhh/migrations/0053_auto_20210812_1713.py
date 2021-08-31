# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2021-08-12 21:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0052_auto_20210803_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipodocumento',
            name='indicaciones',
        ),
        migrations.AddField(
            model_name='tipodocumento',
            name='descripcion',
            field=models.TextField(default=1, max_length=2500, verbose_name='Descripción'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='afp',
            name='descripcion',
            field=models.TextField(default=1, max_length=2500, verbose_name='Descripción'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='afp',
            name='nombre',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='areatitulo',
            name='descripcion',
            field=models.TextField(max_length=2500, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='areatitulo',
            name='nombre',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='colegio',
            name='estado',
            field=models.CharField(choices=[('particular', 'Particular'), ('gratuito', 'Gratuito'), ('particular_subvencionado', 'Particular Subvencionado')], default='particular_subvencionado', max_length=25),
        ),
        migrations.AlterField(
            model_name='documentofuncionario',
            name='tipo_documento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rrhh.TipoDocumento'),
        ),
        migrations.AlterField(
            model_name='especialidad',
            name='descripcion',
            field=models.TextField(max_length=2500, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='especialidad',
            name='nombre',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='funcion',
            name='descripcion',
            field=models.TextField(default=1, max_length=2500, verbose_name='Descripción'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='funcion',
            name='nombre',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='isapre',
            name='descripcion',
            field=models.TextField(default=1, max_length=2500, verbose_name='Descripción'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='isapre',
            name='nombre',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='mencion',
            name='descripcion',
            field=models.TextField(max_length=2500, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='mencion',
            name='nombre',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='tipo_perfil',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Docente'), (2, 'Capellán'), (3, 'Jefe de UTP'), (4, 'Inspector General'), (5, 'Director'), (6, 'Departamental'), (7, 'Asesor'), (8, 'Administrador')], default=1, verbose_name='Tipo de perfil'),
        ),
        migrations.AlterField(
            model_name='tipodocumento',
            name='nombre',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='tipolicencia',
            name='descripcion',
            field=models.TextField(max_length=2500, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='tipolicencia',
            name='nombre',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='tipotitulo',
            name='descripcion',
            field=models.TextField(max_length=2500, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='tipotitulo',
            name='nombre',
            field=models.CharField(max_length=250),
        ),
    ]