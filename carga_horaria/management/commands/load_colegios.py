import csv
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from guardian.shortcuts import assign_perm
from carga_horaria.models import Colegio, Fundacion


class Command(BaseCommand):
    help = 'Loads Colegios, Fundaciones and Users from colegio.csv'

    def handle(self, *args, **options):
        with open('colegios.csv') as f:
            for row in csv.DictReader(f):
                fundacion, _ = Fundacion.objects.get_or_create(nombre=row['Fundación'])
                colegio, _ = Colegio.objects.get_or_create(nombre=row['Nombre Colegio'],
                                                           abrev=row['Abreviación'],
                                                           fundacion=fundacion)
                user, _ = get_user_model().objects.get_or_create(username=row['Usuario'], is_staff=False)
                user.set_password(row['Contraseña'])
                user.save()

                permission = 'change_colegio'
                assign_perm(permission, user, colegio)
                print("Loaded user {} with permission {} on {}".format(user.username, permission, colegio))
