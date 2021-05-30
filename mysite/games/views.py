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
                login(request, user)
        elif 'logout' in request.POST.keys():
            logout(request)

    if request.user.is_authenticated:
        loggedIn = True;
    else:
        loggedIn = False;


    # return HttpResponse("Welcome to the home page!")
    allMatches = Match.objects.all()
    # for match in allMatches:
    #     print("Another match between " + match.player1.username + " and " + match.player2.username)
    #     print(match.player2.username == "Dummy")
    allProfiles = Profile.objects.all() #like a list
    context = {'allMatches': allMatches,
    'allProfiles': allProfiles,
    'loggedIn': loggedIn,
    }
    return render(request, 'games/index.html', context)

def game_pending(request):
    context = {'request_match': None}

    # Create match if user is game creator.
    if 'request_game' in request.GET.keys():
        dummyUser = User.objects.get(username = "Dummy")
        newMatch = Match.objects.get_or_create(player1=request.user, player2=dummyUser, creator=request.user)
        context['request_match'] = newMatch[0]
        print("MATCH CREATED")
        print(context['request_match'].player2.username == "Dummy")

    return render(request, 'games/game_pending.html', context)

def game(request):
    context = {'match':[]}
    if 'matchpk' in request.GET.keys():
        if 'isPlayer1' in request.GET.keys() and request.GET['isPlayer1'] == "False":
            matchpk = request.GET['matchpk']
            match = Match.objects.filter(pk = matchpk)[0]
            match.player2 = request.user
            match.save()
            context['match'] = match

    return render(request, 'games/game.html', context)

def profile(request):
    # return HttpResponse("Hello, world. You're at the profile.")
    return render(request, 'games/profile.html', {})
