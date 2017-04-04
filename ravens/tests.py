from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (views.StartPage)
        yield (views.Introduction)
        yield (views.QuestionPage, {'answer': Constants.answer_keys[self.subsession.round_number-1]})
        yield (views.Results)
