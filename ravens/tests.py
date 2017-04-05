from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        # yield (views.StartPage)
        if self.subsession.round_number == 1:
            yield (views.Introduction)
        yield (views.QuestionPage, {'answer': Constants.answer_keys[self.subsession.round_number-1]})
        if self.subsession.round_number == Constants.num_rounds:
            yield (views.Results)
