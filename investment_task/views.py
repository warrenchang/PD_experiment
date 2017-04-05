from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Investment(Page):
    form_model = models.Player
    form_fields = ['amount_invested']

    def before_next_page(self):
        self.player.random_draw = random.randint(1,10)

        if self.timeout_happened:
            self.player.amount_invested = random.randint(0,21)

        if self.player.amount_invested == 21:
            self.player.success = self.player.random_draw >6
            self.player.payoff = 75*self.player.success
        else:
            self.player.success = self.player.random_draw >5
            self.player.payoff = self.player.amount_invested*self.player.success*3 + 20 - self.player.amount_invested
        # to measure in point
        self.player.payoff /= self.session.config['real_world_currency_per_point']
        self.player.participant.vars['payoff_investment'] = self.player.payoff.to_real_world_currency(self.session)


class Results(Page):
    timeout_seconds = 60

    def vars_for_template(self):
        return {
            'earnings': self.player.payoff.to_real_world_currency(self.session)
                }


page_sequence = [
    Investment,
    Results
]
