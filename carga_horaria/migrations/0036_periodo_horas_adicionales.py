# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-08-31 17:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carga_horaria', '0035_profesor_directivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodo',
            name='horas_adicionales',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]
