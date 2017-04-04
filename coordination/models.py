from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Huanren Zhang'

doc = """
Stag-hunt game to measure the tolerance of strategic uncertainty
"""


class Constants(BaseConstants):
    name_in_url = 'my_coordination'
    players_per_group = 2
    num_rounds = 2

    # payoff matrices for different rounds
    payoff_matrix = {'1':{
        'X':
            {
                'X': 900,
                'Y': 0
            },
        'Y':
            {
                'X': 450,
                'Y': 450
            }
    },
        '2': {
            'X':
                {
                    'X': 550,
                    'Y': 550
                },
            'Y':
                {
                    'X': 100,
                    'Y': 1000
                }
        }
    }


class Subsession(BaseSubsession):
    def before_session_starts(self):
        # this is run before the start of every round
        self.group_randomly()
        if self.round_number == 1:
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round  # pick a random round for payment
            self.session.vars['num_subjects'] = len(self.get_players())


class Group(BaseGroup):
    def interact(self):
        p1,p2 = self.get_players()

        # first calculate payoff
        p1.other_action = p2.action
        p2.other_action = p1.action
        num_X = sum([p.action=='X' for p in p1.subsession.get_players()])
        p1.num_X = num_X
        p2.num_X = num_X
        p1.other_X = num_X - (p1.action=='X')
        p2.other_X = num_X - (p2.action=='X')

        if self.round_number == self.session.vars['paying_round']:
            p1.participant.vars['action_PartII'] = p1.action
            p2.participant.vars['action_PartII'] = p2.action
            p1.participant.vars['other_action_PartII'] = p1.other_action
            p2.participant.vars['other_action_PartII'] = p2.other_action
            p1.participant.vars['guess_PartII'] = p1.guess
            p2.participant.vars['guess_PartII'] = p2.guess
            p1.participant.vars['otherX_PartII'] = p1.other_X
            p2.participant.vars['otherX_PartII'] = p2.other_X
            p1.participant.vars['payoff_from_action'] = c((Constants.payoff_matrix[str(self.round_number)][p1.action][p1.other_action]))
            p2.participant.vars['payoff_from_action'] = c((Constants.payoff_matrix[str(self.round_number)][p2.action][p2.other_action]))
            p1.participant.vars['payoff_from_guess'] = c(max(3 - abs(p1.guess - p1.other_X), 0)*100)
            p2.participant.vars['payoff_from_guess'] = c(max(3 - abs(p2.guess - p2.other_X), 0)*100)
            p1.payoff  = p1.participant.vars['payoff_from_action'] + p1.participant.vars['payoff_from_guess']
            p2.payoff  = p2.participant.vars['payoff_from_action'] + p2.participant.vars['payoff_from_guess']
            # p1.participant.vars['payoff_PartII'] = p1.payoff * self.session.config['real_world_currency_per_point']
            # p2.participant.vars['payoff_PartII'] = p2.payoff * self.session.config['real_world_currency_per_point']


        # print((self.round_number,p1.payoff,p2.payoff))
        # print((p1.participant.id_in_session,p1.action,p1.payoff,p1.signal,p2.participant.id_in_session,p2.action,p2.payoff,p2.signal))


class Player(BasePlayer):
    action = models.CharField(
        choices=['X', 'Y'],
        doc="""This player's action""",
        widget=widgets.RadioSelect()
    )

    guess = models.IntegerField(min=0)
    num_X = models.PositiveIntegerField()
    other_X = models.PositiveIntegerField()

    def get_partner(self):
        return self.get_others_in_group()[0]

