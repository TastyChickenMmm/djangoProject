from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile (models.Model):
    numWins = models.IntegerField(default = 0)
    numLosses = models.IntegerField(default = 0)
    numDraws = models.IntegerField(default = 0)

    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        primary_key = True,
    )
    def __str__(self):
        return self.user.username
    def numGames(self):
        return numWins + numDraws + numLosses
    def winLossRation(self):
        if numLosses != 0:
            return numWins / numLosses
        return float('inf')

# multiple games = multiple models

class Match(models.Model):
    # ForeignKey = one-to-many
    player1 = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'player1',
    )
    player2 = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'player2',
    )

    creator = models.ForeignKey(
        User,
        default = 1,
        on_delete = models.CASCADE,
        related_name = 'creator',
    )

    PLAYER_1_WINS = models.BooleanField(default = False)

    # def __str__(self):
    #     return self.player1.username + " vs. " + self.player2.username
