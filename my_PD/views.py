from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import random


class BasePage(Page):
    def vars_for_template(self):
        v =  {
            'treatment': self.session.config['treatment'],
        }
        v.update(self.extra_vars_for_template())
        return v

    def extra_vars_for_template(self):
        return {}


class BaseWaitPage(WaitPage):
    def vars_for_template(self):
        return {
            'treatment': self.session.config['treatment'],
        }


class Introduction(BasePage):
    timeout_seconds = 30

    def is_displayed(self):
        if self.round_number == 1:
            print('This is the start of PD')
        return self.round_number == 1 and (not self.session.config['debug'])
        # return self.round_number == 1


class Decision(BasePage):
    # timeout_seconds = 30
    form_model = models.Player
    form_fields = ['action']

    def before_next_page(self):
        if self.timeout_happened:
            self.player.action = random.choice(['A','B'])


class DecisionWaitPage(BaseWaitPage):
    template_name = 'my_PD90/DecisionWaitPage.html'

    def after_all_players_arrive(self):
        # it only gets executed once
        self.group.interact()
        # print('players have interacted!')


class Signal(BasePage):
    # timeout_seconds = 30
    form_model = models.Player
    form_fields = ['message']

    def is_displayed(self):
        return self.session.config['treatment'] == "COM"

    def before_next_page(self):
        if self.timeout_happened:
            self.player.message = random.choice(['a','b'])


class SignalWaitPage(BaseWaitPage):
    template_name = 'my_PD90/SignalWaitPage.html'

    def is_displayed(self):
        return self.session.config['treatment'] == "COM"

    def after_all_players_arrive(self):
        self.group.send_message()
        # print('message is sent!')


class Results(BasePage):
    timeout_seconds = 8


class Continuation(BasePage):
    timeout_seconds = 8

    def is_displayed(self):
        return Constants.number_sequence[self.subsession.round_number-1] <= 6

    def extra_vars_for_template(self):
        return {
            'number_generated': Constants.number_sequence[self.player.round_number-1],
        }


class InteractionResults(BasePage):
    timeout_seconds = 30

    def is_displayed(self):
        return Constants.number_sequence[self.subsession.round_number-1] > 6

    def extra_vars_for_template(self):
        return {
            'number_generated': Constants.number_sequence[self.player.round_number-1],
        }


class RematchingWaitPage(WaitPage):
    # template_name = 'my_PD90/SignalWaitPage.html'
    template_name = 'my_PD90/RematchingWaitPage.html'
    wait_for_all_groups = True

    def is_displayed(self):
         return Constants.number_sequence[self.subsession.round_number-1] > 6  # and self.round_number != Constants.num_rounds

    def after_all_players_arrive(self):
        self.subsession.group_randomly()  # randomly rematching
        print((self.subsession.round_number,'Group randomly rematched'))
        if self.round_number == Constants.num_rounds:
            for p in self.subsession.get_players():
                p.participant.vars['payoff_PD'] = sum([this_player.payoff for this_player in p.in_all_rounds()])
                print(('my_PD_RematchingWaitPage',self.round_number,p,sum([this_player.payoff for this_player in p.in_all_rounds()])),p.participant.vars['payoff_PD'])

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
