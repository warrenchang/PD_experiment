from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import random

class StartPage(Page):
    def is_displayed(self):
        if self.round_number == 1:
            print('This is the start of PD practice')
        return self.round_number == 1


class Decision(Page):
    # timeout_seconds = 30
    form_model = models.Player
    form_fields = ['action']

    def before_next_page(self):
        if self.timeout_happened:
            self.player.action = random.choice(['A','B'])
        self.player.interact()


class Signal(Page):
    # timeout_seconds = 30
    form_model = models.Player
    form_fields = ['message']

    def before_next_page(self):
        if self.timeout_happened:
            self.player.message = random.choice(['a', 'b'])
        self.player.send_message()


class Results(Page):
    timeout_seconds = 10


class Continuation(Page):
    timeout_seconds = 5

    def is_displayed(self):
        return Constants.number_sequence[self.subsession.round_number-1] <= 6

    def vars_for_template(self):
        return {
            'number_generated': Constants.number_sequence[self.player.round_number-1],
        }


class InteractionResults(Page):
    timeout_seconds = 45

    def is_displayed(self):
        return Constants.number_sequence[self.subsession.round_number-1] > 6

    def vars_for_template(self):
        return {
            'number_generated': Constants.number_sequence[self.player.round_number-1],
        }


class RematchingWaitPage(WaitPage):
    # template_name = 'my_PD/SignalWaitPage.html'
    template_name = 'my_PD_practice/RematchingWaitPage.html'
    wait_for_all_groups = True

    def is_displayed(self):
         return Constants.number_sequence[self.subsession.round_number-1] > 6  # and self.round_number != Constants.num_rounds

    def after_all_players_arrive(self):
        if self.round_number == Constants.num_rounds:
            for p in self.subsession.get_players():
                p.participant.vars['payoff_PD'] = sum([this_player.payoff for this_player in p.in_all_rounds()])


page_sequence = [
    StartPage,
    Decision,
    Signal,
    Results,
    Continuation,
    InteractionResults,
    RematchingWaitPage
]
