# Generated by Django 2.2 on 2021-09-03 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallecolegio',
            name='estado',
            field=models.CharField(choices=[('particular', 'Particular'), ('particular_subvencionado', 'Particular Subvencionado'), ('gratuito', 'Gratuito')], default='particular_subvencionado', max_length=50),
        ),
        migrations.AlterField(
            model_name='entidad',
            name='dependiente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rrhh.Entidad', verbose_name='Depende de'),
        ),
    ]