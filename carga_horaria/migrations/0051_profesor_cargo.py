# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-09-29 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carga_horaria', '0050_auto_20200929_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='profesor',
            name='cargo',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Docente'), (2, 'Rector'), (3, 'Director'), (4, 'Subdirector'), (5, 'Inspector General'), (6, 'Jefe de UTP'), (7, 'Capellán')], default=1),
        ),
    ]
