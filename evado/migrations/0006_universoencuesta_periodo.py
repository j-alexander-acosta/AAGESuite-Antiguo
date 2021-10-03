# Generated by Django 2.2 on 2021-09-27 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evado', '0005_auto_20210927_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='universoencuesta',
            name='periodo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='evado.PeriodoEncuesta', verbose_name='Periodo de encuesta'),
            preserve_default=False,
        ),
    ]
