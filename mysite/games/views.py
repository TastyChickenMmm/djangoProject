from django.shortcuts import render
from django.http import HttpResponse


# Weite views here
def home(request):
    # return HttpResponse("Welcome to the home page!")
    return render(request, 'games/index.html', {})

def game(request):
    # return HttpResponse("Hello, world. You're at the game.")
    return render(request, 'games/game.html', {})

def profile(request):
    # return HttpResponse("Hello, world. You're at the profile.")
    return render(request, 'games/profile.html', {})
