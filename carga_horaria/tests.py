from django.test import TestCase
from model_mommy import mommy


class TestProfesorModel(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestProfesorModel, cls).setUpClass()
        # TODO: test Kinder to B4

        # colegios
        colegio_impeque = mommy.make(
            'carga_horaria.Colegio',
            prioritarios=79
        )
        colegio_vulnerable = mommy.make(
            'carga_horaria.Colegio',
            prioritarios=80
        )

        # planes
        plan_impeque = mommy.make(
            'carga_horaria.Plan',
            nivel='B1',
            colegio=colegio_impeque
        )
        plan_impeque_igual = mommy.make(
            'carga_horaria.Plan',
            nivel='B5',
            colegio=colegio_vulnerable
        )
        plan_vulnerable = mommy.make(
            'carga_horaria.Plan',
            nivel='B1',
            colegio=colegio_vulnerable
        )

        # cursos
        periodo_impeque = mommy.make(
            'carga_horaria.Periodo',
            plan=plan_impeque,
            colegio=colegio_impeque
        )
        periodo_impeque_igual = mommy.make(
            'carga_horaria.Periodo',
            plan=plan_impeque_igual,
            colegio=colegio_vulnerable
        )
        periodo_vulnerable = mommy.make(
            'carga_horaria.Periodo',
            plan=plan_vulnerable,
            colegio=colegio_vulnerable
        )

        # asignaturas
        cls.horas_impeque = 11
        cls.horas_impeque_igual = 5
        cls.horas_vulnerable = 6

        asignatura_impeque = mommy.make(
            'carga_horaria.Asignatura',
            base__plan=plan_impeque,
            base__horas_jec=cls.horas_impeque,
            horas=cls.horas_impeque
        )
        asignatura_impeque_igual = mommy.make(
            'carga_horaria.Asignatura',
            base__plan=plan_impeque_igual,
            base__horas_jec=cls.horas_impeque_igual,
            horas=cls.horas_impeque_igual
        )
        asignatura_vulnerable = mommy.make(
            'carga_horaria.Asignatura',
            base__plan=plan_vulnerable,
            base__horas_jec=cls.horas_vulnerable,
            horas=cls.horas_vulnerable
        )

        # associate periodos with asignaturas
        asignatura_impeque.periodos.add(periodo_impeque)
        asignatura_impeque_igual.periodos.add(periodo_impeque_igual)
        asignatura_vulnerable.periodos.add(periodo_vulnerable)

        # profesores
        cls.profesor_impeque = mommy.make(
            'carga_horaria.Profesor',
            colegio=colegio_impeque,
            horas=44  # LEGACY HOURS
        )
        cls.profesor_impeque_igual = mommy.make(
            'carga_horaria.Profesor',
            colegio=colegio_vulnerable,
            horas=44  # LEGACY HOURS
        )
        cls.profesor_vulnerable = mommy.make(
            'carga_horaria.Profesor',
            colegio=colegio_vulnerable,
            horas=44  # LEGACY HOURS
        )
        cls.profesor_mestizo = mommy.make(
            'carga_horaria.Profesor',
            colegio=colegio_vulnerable,
            horas=44  # LEGACY HOURS
        )

        # asignaciones profesor impeque
        mommy.make(
            'carga_horaria.Asignacion',
            profesor=cls.profesor_impeque,
            asignatura=asignatura_impeque,
            curso=periodo_impeque,
            horas=asignatura_impeque.horas
        )

        # asignaciones profesor impeque igual
        mommy.make(
            'carga_horaria.Asignacion',
            profesor=cls.profesor_impeque_igual,
            asignatura=asignatura_impeque_igual,
            curso=periodo_impeque_igual,
            horas=asignatura_impeque_igual.horas
        )

        # asignaciones profesor vulnerable
        mommy.make(
            'carga_horaria.Asignacion',
            profesor=cls.profesor_vulnerable,
            asignatura=asignatura_vulnerable,
            curso=periodo_vulnerable,
            horas=asignatura_vulnerable.horas
        )

        # asignaciones profesor mestizo
        mommy.make(
            'carga_horaria.Asignacion',
            profesor=cls.profesor_mestizo,
            asignatura=asignatura_impeque_igual,
            curso=periodo_impeque_igual,
            horas=asignatura_impeque_igual.horas
        )
        mommy.make(
            'carga_horaria.Asignacion',
            profesor=cls.profesor_mestizo,
            asignatura=asignatura_vulnerable,
            curso=periodo_vulnerable,
            horas=asignatura_vulnerable.horas
        )

    def test_65_35(self):
        self.assertEqual(self.profesor_impeque.horas_docentes, self.horas_impeque)
        self.assertEqual(self.profesor_impeque_igual.horas_docentes, self.horas_impeque_igual)

    def test_60_40(self):
        self.assertEqual(self.profesor_vulnerable.horas_docentes, self.horas_vulnerable)

    def test_mestizaje(self):
        self.assertEqual(self.profesor_mestizo.horas_docentes, self.horas_impeque_igual+self.horas_vulnerable)
