from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):
    def play_round(self):
        if self.subsession.round_number == 1 and (not self.session.config['debug']):
            yield(views.Introduction)
        yield (views.Decision, {"action": random.choice(['A','B'])})
        if self.session.config['treatment'] == 'COM':
            yield (views.Signal, {"message": random.choice(['a','b'])})
        yield (views.Results)
        if Constants.number_sequence[self.subsession.round_number-1] > 9:
            yield (views.InteractionResults)
        else:
            yield (views.Continuation)

