from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile, Match
from django.utils import timezone
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
import pprint
import random



def home(request):
    # Check whether user has just logged in or out.
    if request.POST:
        if 'inputUsername' in request.POST.keys():
            user = authenticate(username=request.POST['inputUsername'],
            password=request.POST['inputPassword'])
            if user is not None:
                login(request, user)
        elif 'logout' in request.POST.keys():
            logout(request)

    # Determine if user is logged in.
    if request.user.is_authenticated:
        loggedIn = True;
    else:
        loggedIn = False;


    allMatches = Match.objects.all()
    thisUser = request.user
    context = {'allMatches': allMatches,
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

    # Determine which match this is.
    if 'matchpk' in request.GET.keys():
        matchpk = request.GET['matchpk']
        match = Match.objects.filter(pk = matchpk)[0]
        if 'isPlayer1' in request.GET.keys() and request.GET['isPlayer1'] == "False":
            # This is player 2, so update the match info.
            match.player2 = request.user
            match.save()
        context['match'] = match
        print("The match is")
        print(context['match'])
    else:
        print("Error in game view: cannot find matchpk in request.GET.keys()")

    # Someone just moved
    if 'moved' in request.POST.keys():
        match.PLAYER_1_MOVE = not match.PLAYER_1_MOVE # Update whose move it is.

        # Apply algorithm to determine if it's a winning move.
        winningMoveDieRoll = random.random() # Random number from 0 to 1.
        print("winningMoveDieRoll = " + str(winningMoveDieRoll))
        if winningMoveDieRoll < 0.3:
            # This is a winning move.

            match.GAME_WON = True # Update match

            # Locate the profiles of players
            player1Profile = Profile.objects.filter(user = match.player1)[0]
            player2Profile = Profile.objects.filter(user = match.player2)[0]

            # Update profiles
            if match.player1 == request.user:
                # User is player 1
                match.PLAYER_1_WINS = True
                player1Profile.numWins += 1
                player2Profile.numLosses += 1
                print("PLAYER 1 WINS")
            else:
                # User is player 2
                match.PLAYER_1_WINS = False
                player1Profile.numLosses += 1
                player2Profile.numWins += 1
                print("PLAYER 2 WINS")

        # Save changes to models
        match.save()
        player1Profile.save()
        player2Profile.save()

    return render(request, 'games/game.html', context)

def profile(request):
    context = {'userProfile': None}

    # Locate profile from the user's pk
    if 'userPK' in request.POST.keys():
        userPK = request.POST['userPK'] # Find user's pk
        thisUser = User.objects.filter(pk = userPK)[0] # Locate user from user's pk
        userProfile = Profile.objects.filter(user = thisUser)[0] # Locate profile from user
        context['userProfile'] = userProfile
    else:
        print("User cannot be found.")

    return render(request, 'games/profile.html', context)
