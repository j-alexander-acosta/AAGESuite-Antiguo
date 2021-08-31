from evado.models import CursoProfesor, AplicarUniversoEncuestaPersona


def profesor_evaluacion_alumno(documento, ue):
    materias_profesor = CursoProfesor.objects.filter(rut__iexact=documento)
    total_encuestas = 0
    total_respuestas = 0
    for x in materias_profesor:
        codigo = x.codigo
        encuestas = AplicarUniversoEncuestaPersona.objects.filter(
            universo_encuesta=ue,
            curso_alumno__cod_curso__iexact=codigo,
            finalizado__isnull=False
        )
        for e in encuestas:
            total_respuestas += e.total_respuestas
        total_encuestas += encuestas.count()
    docente = materias_profesor.first()
    lista = map(lambda x: x.codigo, materias_profesor)
    total_alumnos = AplicarUniversoEncuestaPersona.objects.filter(
        universo_encuesta=ue,
        curso_alumno__cod_curso__in=lista
    ).distinct()
    return {
        'Nombres': docente.nombres, 'Apellidos': docente.apellidos, 'Rut': docente.rut,
        'Total Encuestas': total_encuestas, 'Total Respuestas': total_respuestas,
        'Total Materias': materias_profesor.count(), 'Total Alumnos': total_alumnos.count()
    }
