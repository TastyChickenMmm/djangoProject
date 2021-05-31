from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile, Match
from django.utils import timezone
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
import pprint
import random



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


    allMatches = Match.objects.all()
    allProfiles = Profile.objects.all() #like a list
    thisUser = request.user
    context = {'allMatches': allMatches,
    'allProfiles': allProfiles,
    'loggedIn': loggedIn,
    'thisUser': thisUser,
    }
    return render(request, 'games/index.html', context)

def game_pending(request):
    context = {'request_match': None}

    # Create match if user is game creator.
    if 'request_game' in request.GET.keys():
        dummyUser = User.objects.get(username = "Dummy")
        newMatch = Match.objects.get_or_create(player1=request.user, player2=dummyUser, creator=request.user)
        context['match'] = newMatch[0]
        print("MATCH CREATED")
        print(context['match'].player2.username == "Dummy")

    return render(request, 'games/game_pending.html', context)

def game(request):
    context = {'match': None}
    if 'matchpk' in request.GET.keys():
        matchpk = request.GET['matchpk']
        match = Match.objects.filter(pk = matchpk)[0]
        if 'isPlayer1' in request.GET.keys() and request.GET['isPlayer1'] == "False":
            match.player2 = request.user
            match.save()
        context['match'] = match
        print("The match is")
        print(context['match'])
    else:
        print("Error in game view: cannot find matchpk in request.GET.keys()")

    if 'moved' in request.POST.keys():
        match.PLAYER_1_MOVE = not match.PLAYER_1_MOVE
        winningMoveDieRoll = random.random()
        print("winningMoveDieRoll = " + str(winningMoveDieRoll))
        if winningMoveDieRoll < 0.3:
            match.GAME_WON = True;
            if match.player1 == request.user:
                match.PLAYER_1_WINS = True;
                print("PLAYER 1 WINS")
            else:
                match.PLAYER_1_WINS = False;
                print("PLAYER 2 WINS")
        match.save()


    return render(request, 'games/game.html', context)

def profile(request):
    context = {'userProfile': None}


    if 'userPK' in request.POST.keys():
        userPK = request.POST['userPK']
        thisUser = User.objects.filter(pk = userPK)[0]
        userProfile = Profile.objects.filter(user = thisUser)[0]
        context['userProfile'] = userProfile
    else:
        print("User cannot be found.")

    return render(request, 'games/profile.html', context)
