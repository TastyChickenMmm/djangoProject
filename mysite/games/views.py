from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile, Match
from django.utils import timezone
from django.contrib.auth.models import User, AnonymousUser
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
    for match in allMatches:
        print(match.player2.is_anonymous)
    allProfiles = Profile.objects.all() #like a list
    context = {'allMatches': allMatches,
    'allProfiles': allProfiles,
    'loggedIn': loggedIn,
    }
    return render(request, 'games/index.html', context)

def game(request):
    # return HttpResponse("Hello, world. You're at the game.")
    context = {'match':[]}

    # Create match if user is game creator.
    if 'request_game' in request.GET.keys():
        dummyUser = User.objects.get(username = "Dummy")
        newMatch = Match.objects.get_or_create(player1=request.user, player2=dummyUser, creator=request.user)
        print(request.user)
        context['request_match'] = newMatch

    # Find match if user is game acceptor.
    elif 'matchpk' in request.GET.keys():
        print(request.GET['matchpk'])
        matchpk = request.GET['matchpk']
        match = Match.objects.filter(pk = matchpk)[0]
        match.player2 = request.user
        match.save()
        print("PLAYER 2 HAS BEEN CHANGED TOOOOOOOOO")
        print(match.player2)
        context['match'] = match
        # match.player1 = match.creator
    else:
        print("MATCH NOT FOUND")

    return render(request, 'games/game.html', context)

def profile(request):
    # return HttpResponse("Hello, world. You're at the profile.")
    return render(request, 'games/profile.html', {})
