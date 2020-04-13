from django.shortcuts import render
from .viewsAlexis import *


def home(request):
    return render(request, 'carga_horaria/home.html')
