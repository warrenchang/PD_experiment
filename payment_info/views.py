from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import math


class PaymentInfo(Page):

    def vars_for_template(self):
        participant = self.participant
        print(self.participant.vars)
        return {
            'redemption_code': participant.label or participant.code,
            'total_payoff': self.participant.payoff_plus_participation_fee(),
            'payoff_quiz': participant.vars['payoff_quiz'],
            'payoff_PD': participant.vars['payoff_PD'],
            'real_payoff_PD': participant.vars['payoff_PD'].to_real_world_currency(self.session),
            'payoff_coordination': participant.vars['payoff_coordination'],
            'real_payoff_coordination': participant.vars['payoff_coordination'].to_real_world_currency(self.session),
            'payoff_ravens': participant.vars['payoff_ravens'],
            'payoff_investment': participant.vars['payoff_investment'],
            'participation_fee': self.session.config['participation_fee']
        }


page_sequence = [PaymentInfo]
