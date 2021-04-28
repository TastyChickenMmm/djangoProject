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
