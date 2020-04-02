from django.shortcuts import render


def home(request):
    return render(request, 'scheduler/home.html')
