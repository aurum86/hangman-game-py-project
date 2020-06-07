from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import redirect


def index(request):
    return HttpResponse("Hi, You're at the Hangman game.")


def redirect_view(request):
    return redirect('/hangman/')
