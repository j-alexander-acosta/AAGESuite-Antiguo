# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-10-20 19:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carga_horaria', '0055_auto_20201019_2206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('rut', models.CharField(blank=True, max_length=13, null=True, unique=True)),
                ('adventista', models.BooleanField(default=False)),
            ],
        ),
    ]