from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile, Match
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import pprint



# Write views here
def home(request):
    if request.POST:
        if 'inputUsername' in request.POST.keys():
            user = authenticate(username=request.POST['inputUsername'],
            password=request.POST['inputPassword'])
            if user is not None:
                print("Login successful.")
                login(request, user)
            else:
                print("Failed login.")
        elif 'logout' in request.POST.keys():
            logout(request)

    if request.user.is_authenticated:
        loggedIn = True;
        print("loggedIn = True")
    else:
        loggedIn = False;
        print("loggedIn = False")


    # return HttpResponse("Welcome to the home page!")
    allMatches = Match.objects.all()
    allProfiles = Profile.objects.all() #like a list
    context = {'allMatches': allMatches,
    'allProfiles': allProfiles,
    'loggedIn': loggedIn,
    }
    return render(request, 'games/index.html', context)

def game(request):
    # return HttpResponse("Hello, world. You're at the game.")
    context = {'match':[]}

    if 'matchpk' in request.POST.keys():
        print(request.POST['matchpk'])
        matchpk = request.POST['matchpk']
        match = Match.objects.filter(pk = matchpk)[0]
        print(match)
        context['match'] = match
        # match.player1 = match.creator
    else:
        print("MATCH NOT FOUND")

    return render(request, 'games/game.html', context)

def profile(request):
    # return HttpResponse("Hello, world. You're at the profile.")
    return render(request, 'games/profile.html', {})
