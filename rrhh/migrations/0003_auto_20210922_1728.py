# Generated by Django 2.2 on 2021-09-22 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0002_auto_20210922_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallecolegio',
            name='tipo_subvencion',
            field=models.CharField(choices=[('gratuito', 'Gratuito'), ('particular', 'Particular'), ('particular_subvencionado', 'Particular Subvencionado')], default='particular_subvencionado', max_length=75, verbose_name='Tipo de subvención'),
        ),
    ]