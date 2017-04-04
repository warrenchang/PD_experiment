from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):
    def play_round(self):
        num_participants = len(self.subsession.get_players())
        yield (views.Decision, {"action": random.choice(['X','Y']), "guess": random.randint(0,num_participants-1)})
        yield (views.Results)
