# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2021-05-04 19:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carga_horaria', '0085_auto_20210421_2100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asignacionasistentelog',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='asignacionlog',
            options={'ordering': ('-created_at',)},
        ),
    ]
