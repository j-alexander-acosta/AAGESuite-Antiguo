class Ley20903(object):
    IMPEQUES = {11: (8.25, 0, 0),
                5: (3.75, 0, 0),
                0: (0, 0, 0)}
    VULNERABLES = {6: (4.5, 0, 0),
                   0: (0, 0, 0)}

    def __init__(self, horas_docentes):
        self.horas_docentes = horas_docentes

    @property
    def horas_lectivas(self):
        return self.IMPEQUES[self.horas_docentes][0]

    @property
    def horas_lectivas_vulnerables(self):
        return self.VULNERABLES[self.horas_docentes][0]
