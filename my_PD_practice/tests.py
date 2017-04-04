from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):
    def play_round(self):
        yield (views.StartPage)
        yield (views.Decision, {"action": random.choice(['A','B'])})
        yield (views.Signal, {"message": random.choice(['a','b'])})
        yield (views.Results)
        yield (views.Continuation)
        yield (views.InteractionResults)
