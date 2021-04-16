from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile (models.Model):
    user = models.OneToOneField(
        User,
        # numWins = models.IntegerField,
        # numLosses = models.IntegerField,
        # numDraws = models.IntegerField,
        on_delete = models.CASCADE,
        primary_key = True
    )
    def __str__(self):
        return self.user
    # def numGames(self):
    #     return numWins + numDraws + numLosses
    # def winLossRation(self):
    #     return numWins / numLosses

# multiple games = multiple models

class Match(models.Model):
    # ForeignKey = one-to-many
    player1 = models.ForeignKey(
        User,
        on_delete,
    )
    player2 = models.ForeignKey(
        User,
        on_delete,
    )

    PLAYER_1_WINS = models.BooleanField

    def __str__(self):
        return self.player1 + " vs. " + self.player2
