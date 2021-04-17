from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile, Match


# Weite views here
def home(request):
    # return HttpResponse("Welcome to the home page!")
    allMatches = Match.objects.all()
    allProfiles = Profile.objects.all() #like a list
    context = {'allMatches': allMatches,
    'allProfiles': allProfiles,
    }
    return render(request, 'games/index.html', context)

def game(request):
    # return HttpResponse("Hello, world. You're at the game.")
    return render(request, 'games/game.html', {})

def profile(request):
    # return HttpResponse("Hello, world. You're at the profile.")
    return render(request, 'games/profile.html', {})
