from django.db import models


TIPO_SUBVENCION = {
    ('particular', 'Particular'),
    ('particular_subvencionado', 'Particular Subvencionado'),
    ('gratuito', 'Gratuito'),
}
TIPO_CONTRATO = (
    (1, 'Indefinido'),
    (2, 'A plazo'),
    (3, 'Reemplazo'),
)
TIPO_HORA = (
    (1, 'Sostenedor'),
    (2, 'PIE'),
    (3, 'SEP'),
)
TIPO_JORNADA = (
    ('completa', 'Completa'),
    ('media', 'Media'),
    ('noche', 'Noche'),
)
TIPO_FUNCIONARIO = (
    (1, 'Empleado'),
    (2, 'Misionero')
)
TIPO_MISIONERO = (
    (1, 'Licencia misionera'),
    (2, 'Credencial misionera'),
    (2, 'Credencial ministerial')
)
PREVISION_SALUD = (
    (1, 'Fonasa'),
    (2, 'Isapre'),
)
TIPO_ENTREVISTA = (
    (1, 'Felicitaciones'),
    (2, 'Recomendaciones')
)
RAZON_FINIQUITO = (
    (1, 'Término de contrato'),
    (2, 'Finiquito de mutuo acuerdo'),
    (3, 'Finiquito por parte del empleador'),
    (4, 'Renuncia voluntaria'),
)
ESTADO_SOLICITUD = (
    (1, 'Aceptada'),
    (2, 'Pendiente'),
    (3, 'Rechazada'),
    (4, 'En espera de candidatos'),
    (5, 'Pendiente de aprobación'),
    (6, 'Aprobada, lista para contratar'),
    (7, 'Aprobada y contratado')
)
TIPOS_SOLICITUD = (
    (1, 'Contratación'),
    (2, 'Contratación de reemplazo'),
    (3, 'Renovación de contrato'),
    (4, 'Traslado'),
)
ESTADO_CONTRATACION = (
    (1, 'Iniciado'),
    (2, 'Listo para firmar'),
    (3, 'En revisión'),
    (4, 'Firmado'),
)
DOCUMENTO = (
    (1, 'Toma de conocimiento del Reglamento Interno'),
    (2, 'Autorización de descuento de diezmo'),
    (3, 'Autorización de uso de imagen'),
)


class Funcion(models.Model):
    TIPO_FUNCION = (
        (1, 'Funcion principal'),
        (2, 'Función secundaria')
    )

    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=250, null=True, blank=True, verbose_name="Descripción")
    tipo = models.PositiveSmallIntegerField(default=1, choices=TIPO_FUNCION, verbose_name='Tipo de función')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Función de empleado'
        verbose_name_plural = u'Funciones de empleados'


class TipoLicencia(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(max_length=500, verbose_name='Descripción')
    total_dias = models.IntegerField(verbose_name='Total de días correspondientes')
    dias_habiles = models.BooleanField(default=True, verbose_name='Corresponde a días hábiles')

    def __str__(self):
        return '{} ({}-{})'.format(
                self.nombre,
                self.total_dias,
                '1' if self.dias_habiles else '0'
            )

    class Meta:
        verbose_name = u'Tipo de licencia'
        verbose_name_plural = u'Tipos de licencia'


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=200)
    indicaciones = models.TextField(max_length=2500)

    def __str__(self):
        return '{}'.format(
            self.nombre
        )

    class Meta:
        verbose_name = u'Tipo de documento'
        verbose_name_plural = u'Tipos de documento'


class Banco(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(max_length=2500, verbose_name='Descripción')

    def __str__(self):
        return '{}'.format(
            self.nombre
        )

    class Meta:
        verbose_name = u'Banco'
        verbose_name_plural = u'Bancos'


class AFP(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=250, null=True, blank=True, verbose_name="Descripción")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'AFP'
        verbose_name_plural = u'AFPs'


class Isapre(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=250, null=True, blank=True, verbose_name="Descripción")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = u'Isapre'
        verbose_name_plural = u'Isapres'
