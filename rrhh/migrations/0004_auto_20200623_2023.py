# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-06-23 20:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0003_archivo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Licencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_licencia_descripcion', models.TextField(blank=True, max_length=500, null=True, verbose_name='Tipo de licencia')),
                ('folio_licencia', models.CharField(max_length=30, verbose_name='Folio de la licencia')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de inicio')),
                ('total_feriados', models.IntegerField(default=0, verbose_name='Total de feriados en el periodo de la licencia')),
                ('fecha_termino', models.DateField(blank=True, null=True, verbose_name='Fecha de término')),
                ('total_dias', models.IntegerField(verbose_name='Total de días de licencia')),
            ],
            options={
                'verbose_name': 'Licencia',
                'verbose_name_plural': 'Licencias',
            },
        ),
        migrations.CreateModel(
            name='TipoLicencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('descripcion', models.TextField(max_length=500, verbose_name='Descripción')),
                ('total_dias', models.IntegerField(verbose_name='Total de días correspondientes')),
                ('dias_habiles', models.BooleanField(default=True, verbose_name='Corresponde a días hábiles')),
            ],
            options={
                'verbose_name': 'Tipo de licencia',
                'verbose_name_plural': 'Tipos de licencia',
            },
        ),
        migrations.CreateModel(
            name='Vacacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_dias', models.IntegerField(verbose_name='Total de días de vacaciones')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de inicio')),
                ('total_feriados', models.IntegerField(default=0, verbose_name='Total de feriados en el periodo de vacaciones')),
                ('fecha_termino', models.DateField(blank=True, null=True, verbose_name='Fecha de término')),
                ('es_pendiente', models.BooleanField(default=False, verbose_name='Corresponde a vacaciones pendientes')),
            ],
            options={
                'verbose_name': 'Vacación',
                'verbose_name_plural': 'Vacaciones',
            },
        ),
        migrations.AlterModelOptions(
            name='entrevista',
            options={'verbose_name': 'Funcionario', 'verbose_name_plural': 'Funcionarios'},
        ),
        migrations.RenameField(
            model_name='funcionario',
            old_name='nombre',
            new_name='apellido_materno',
        ),
        migrations.RenameField(
            model_name='funcionario',
            old_name='sexo',
            new_name='apellido_paterno',
        ),
        migrations.RemoveField(
            model_name='funcionario',
            name='fecha_ingreso',
        ),
        migrations.AddField(
            model_name='funcionario',
            name='antiguedad_docente_meses',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Meses de antiguedad como docente'),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='antiguedad_sea_meses',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Meses de antiguedad en el SEA'),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='casa_formadora',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='fecha_ingreso_docente',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de ingreso como docente'),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='fecha_ingreso_sea',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de ingreso al SEA'),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='genero',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='funcionario',
            name='nombres',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='direccion',
            field=models.CharField(max_length=255, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='estado_civil',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='nacionalidad',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='religion',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Religión'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='telefono',
            field=models.CharField(max_length=15, verbose_name='Teléfono'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='titulo',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Título'),
        ),
        migrations.AddField(
            model_name='vacacion',
            name='funcionario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.Funcionario'),
        ),
        migrations.AddField(
            model_name='licencia',
            name='funcionario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.Funcionario'),
        ),
        migrations.AddField(
            model_name='licencia',
            name='tipo_licencia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rrhh.TipoLicencia', verbose_name='Tipo de licencia'),
        ),
    ]
