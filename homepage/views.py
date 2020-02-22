from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {'pageheader': 'Dashboard'})


def authenticate_twitter(request):
    return HttpResponse('Will authenticate now')
