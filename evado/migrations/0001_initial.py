# Generated by Django 2.2 on 2021-09-21 18:57

from django.db import migrations, models
import django.db.models.deletion
import evado.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rrhh', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AplicarUniversoEncuestaPersona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(default=evado.models.generate_hash, max_length=128, null=True, unique=True, verbose_name='hash')),
                ('comentario', models.TextField(blank=True, null=True)),
                ('finalizado', models.DateTimeField(blank=True, null=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('evaluado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluado', to='rrhh.Persona')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.Persona')),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaPregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ConfigurarEncuestaUniversoPersona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('evaluados', models.ManyToManyField(related_name='evaluados', to='rrhh.Persona')),
            ],
        ),
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PeriodoEncuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('activo', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PreguntaEncuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregunta', models.TextField()),
                ('es_respuesta_directa', models.BooleanField(default=False)),
                ('no_mostrar_pregunta', models.BooleanField(default=False)),
                ('requerida', models.BooleanField(default=True, verbose_name='Es requerida')),
                ('numero_pregunta', models.PositiveIntegerField(verbose_name='Número de pregunta')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evado.CategoriaPregunta')),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta', models.CharField(max_length=255)),
                ('columna', models.PositiveIntegerField(default=1)),
                ('peso', models.IntegerField(default=0)),
                ('escrita', models.BooleanField(default=False, verbose_name='Es escrita')),
                ('check', models.BooleanField(default=False, verbose_name='Es seleccionable')),
            ],
        ),
        migrations.CreateModel(
            name='TipoDescripcionItemPregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoRespuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoUniversoEncuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('codigo', models.CharField(choices=[('EN0002', 'Evaluación Personalizada')], max_length=10, unique=True, verbose_name='Código')),
            ],
        ),
        migrations.CreateModel(
            name='UniversoEncuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido_email', models.TextField(verbose_name='Contenido del correo electrónico')),
                ('inicio', models.DateField()),
                ('fin', models.DateField()),
                ('activar_campo_comentario', models.BooleanField(default=False)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('correos_enviados', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de envío de correos')),
                ('creado', models.BooleanField(default=False)),
                ('config_universo_persona', models.ManyToManyField(to='evado.ConfigurarEncuestaUniversoPersona', verbose_name='Evaluadores')),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evado.Encuesta')),
                ('tipo_encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evado.TipoUniversoEncuesta', verbose_name='Tipo de encuesta')),
            ],
            options={
                'ordering': ['creado_en'],
            },
        ),
        migrations.CreateModel(
            name='RespuestaAplicarUniversoEncuestaPersona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta_directa', models.TextField(blank=True, null=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('aplicar_universo_encuesta_persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evado.AplicarUniversoEncuestaPersona')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evado.PreguntaEncuesta')),
                ('respuesta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='evado.Respuesta')),
            ],
            options={
                'verbose_name': 'Respuesta a Encuesta',
                'verbose_name_plural': 'Respuestas a Encuestas',
            },
        ),
        migrations.AddField(
            model_name='respuesta',
            name='tipo_respuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evado.TipoRespuesta', verbose_name='Tipo de respuesta'),
        ),
        migrations.AddField(
            model_name='preguntaencuesta',
            name='descripcion_item_pregunta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evado.TipoDescripcionItemPregunta', verbose_name='Descripción de ítem de pregunta'),
        ),
        migrations.AddField(
            model_name='preguntaencuesta',
            name='encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evado.Encuesta'),
        ),
        migrations.AddField(
            model_name='preguntaencuesta',
            name='tipo_respuesta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evado.TipoRespuesta', verbose_name='Tipo de respuesta'),
        ),
        migrations.CreateModel(
            name='PersonaUniversoEncuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo_enviado', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de envío de correo')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.Persona')),
                ('universo_encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evado.UniversoEncuesta', verbose_name='Universo de encuestas')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='InfoPersona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('funcion', models.CharField(blank=True, max_length=100, null=True)),
                ('colegio', models.CharField(blank=True, max_length=100, null=True)),
                ('fundacion', models.CharField(blank=True, max_length=100, null=True)),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='rrhh.Persona')),
            ],
            options={
                'verbose_name': 'Información extra de Persona',
                'verbose_name_plural': 'Información extra de Personas',
            },
        ),
        migrations.CreateModel(
            name='DescripcionItemPregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('tipo_descripcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evado.TipoDescripcionItemPregunta', verbose_name='Tipo de descripción')),
            ],
        ),
        migrations.CreateModel(
            name='CorreoUniversoEncuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encabezado', models.CharField(max_length=255)),
                ('correo', models.TextField()),
                ('enviado', models.DateTimeField(blank=True, null=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('universo_encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evado.UniversoEncuesta')),
            ],
            options={
                'verbose_name': 'Correo Universo Encuesta',
                'verbose_name_plural': 'Correos de universos de encuestas',
            },
        ),
        migrations.AddField(
            model_name='configurarencuestauniversopersona',
            name='periodo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='evado.PeriodoEncuesta'),
        ),
        migrations.AddField(
            model_name='configurarencuestauniversopersona',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persona', to='rrhh.Persona', verbose_name='Evaluador'),
        ),
        migrations.AddField(
            model_name='configurarencuestauniversopersona',
            name='tipo_encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evado.TipoUniversoEncuesta', verbose_name='Tipo de encuesta'),
        ),
        migrations.AddField(
            model_name='aplicaruniversoencuestapersona',
            name='universo_encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evado.UniversoEncuesta'),
        ),
    ]
