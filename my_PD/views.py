from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    timeout_seconds = 10

    def is_displayed(self):
        return self.round_number == 1


class Decision(Page):
    # timeout_seconds = 30
    form_model = models.Player
    form_fields = ['action']


class DecisionWaitPage(WaitPage):
    template_name = 'my_PD/DecisionWaitPage.html'

    def after_all_players_arrive(self):
        # it only gets executed once
        self.group.interact()
        print('players have interacted!')


class Signal(Page):
    # timeout_seconds = 30
    form_model = models.Player
    form_fields = ['message']


class SignalWaitPage(WaitPage):
    template_name = 'my_PD/SignalWaitPage.html'

    def after_all_players_arrive(self):
        self.group.send_message()
        print('message is sent!')


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
    template_name = 'my_PD/RematchingWaitPage.html'
    wait_for_all_groups = True

    def is_displayed(self):
         return Constants.number_sequence[self.subsession.round_number-1] > 6  # and self.round_number != Constants.num_rounds

    def after_all_players_arrive(self):
        self.subsession.group_randomly()  # randomly rematching
        print('Group randomly rematched')
        if self.round_number == Constants.num_rounds:
            for p in self.subsession.get_players():
                p.participant.vars['payoff_PD'] = sum([this_player.payoff for this_player in p.in_all_rounds()])
                print((p,sum([this_player.payoff for this_player in p.in_all_rounds()])),p.participant.vars['payoff_PD'])

page_sequence = [
    Introduction,
    Decision,
    DecisionWaitPage,
    Signal,
    SignalWaitPage,
    Results,
    Continuation,
    InteractionResults,
    RematchingWaitPage
]
