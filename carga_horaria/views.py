from django.shortcuts import render


def home(request):
    return render(request, 'carga_horaria/home.html')

