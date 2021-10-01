# Generated by Django 2.2 on 2021-09-30 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0004_auto_20210927_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallecolegio',
            name='tipo_subvencion',
            field=models.CharField(choices=[('particular_subvencionado', 'Particular Subvencionado'), ('particular', 'Particular'), ('gratuito', 'Gratuito')], default='particular_subvencionado', max_length=75, verbose_name='Tipo de subvención'),
        ),
    ]
