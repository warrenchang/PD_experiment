from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random

class StartPage(Page):
    def is_displayed(self):
        if self.round_number == 1:
            print('This is the start of Ravens tests')
        return self.round_number == 1 and (not self.session.config['debug'])


class Introduction(Page):
    timeout_seconds = 60

    def is_displayed(self):
        return self.round_number == 1


class QuestionPage(Page):
    timeout_seconds = 60
    form_model = models.Player
    form_fields = ['answer']

    def vars_for_template(self):
        return {'image_path': 'ravens/{}.jpg'.format(self.round_number)}

    def before_next_page(self):
        if self.timeout_happened:
            self.player.answer = random.randint(1,8)
        self.player.ans_correct = self.player.answer == Constants.answer_keys[self.round_number-1]
        self.player.participant.vars['payoff_ravens'] += self.player.ans_correct*2
        self.player.payoff = self.player.ans_correct*2 / self.session.config['real_world_currency_per_point'] # to measure in point


class Results(Page):
    timeout_seconds = 60

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'total_correct': sum([p.ans_correct for p in self.player.in_all_rounds()]),
            'earnings': sum([p.ans_correct for p in self.player.in_all_rounds()])*2,
                }

    def before_next_page(self):
        for p in self.subsession.get_players():
            p.participant.vars['payoff_ravens'] = sum([p.ans_correct for p in self.player.in_all_rounds()])*2


page_sequence = [
    # StartPage,
    Introduction,
    QuestionPage,
    Results
]
