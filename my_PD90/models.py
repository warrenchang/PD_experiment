from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Huanren Zhang'

doc = """
This is an infinitely repeated "Prisoner's Dilemma" with private monitoring.
"""


class Constants(BaseConstants):
    name_in_url = 'my_PD90'
    players_per_group = 2

    number_sequence = [6, 2, 1, 5, 7, 5, 3, 3, 2, 4, 5, 8, 9, 10, 3, 6, 1,
                       5, 5, 6, 4, 8, 10, 1, 3, 6, 5, 10, 2, 3, 5, 6, 1, 6,
                       4, 6, 1, 9, 4, 6, 6, 4, 2, 6, 8, 1, 4, 2, 3, 4, 3,
                       10, 5, 4, 1, 8, 5, 4, 7, 10, 3, 7, 1, 6, 4, 5, 8, 9,
                       2, 6, 10, 2, 1, 5, 9, 3, 2, 2, 5, 10, 2, 2, 5, 5, 10,
                       4, 2, 9, 6, 3, 5, 10, 2, 7, 3, 4, 6, 9, 10]
    interactions = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4,
                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                    4, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6,
                    6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8,
                    9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10]
    round_in_interactions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 1, 2, 3,
                             4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6,
                             7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                             24, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8,
                             9, 10, 11, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5,
                             1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7]
    interaction_length = [14, 9, 5, 24, 8, 11, 9, 5, 7, 7]
    num_rounds = 99  # change num_rounds for testing purpose, but need to make sure that number_sequence
    num_interactions = interactions[num_rounds - 1]

    epsilon = 0.45
    gamma = 0.05

    instructions_template = 'my_PD90/Instructions.html'

    # payoff for the prisoner's dilemma
    R = 130
    T = 150
    S = 5
    P = 30

    payoff_matrix = {
        'A':
            {
                'A': R,
                'B': S
            },
        'B':
            {
                'A': T,
                'B': P
            }
    }


class Subsession(BaseSubsession):
    def before_session_starts(self):
        # this is run before the start of every round

        current_round_in_interaction = Constants.round_in_interactions[self.round_number-1]

        if current_round_in_interaction == 1: # at the start of each interaction, reshuffle group
            self.group_randomly()
        else:  # otherwise, group structure is the same as in the previous round
            self.group_like_round(self.round_number-1)

        for p in self.get_players(): # set interaction number and round number
            p.interaction_number = Constants.interactions[p.round_number-1]
            p.round_in_interaction = Constants.round_in_interactions[p.round_number-1]
            # print((p.interaction_number,p.round_in_interaction))


class Group(BaseGroup):
    def interact(self):
        p1,p2 = self.get_players()
        p1.my_id = p1.participant.id_in_session
        p2.my_id = p2.participant.id_in_session
        p1.partner_id = p2.my_id
        p2.partner_id = p1.my_id

        # first calculate payoff
        p1.other_action = p2.action
        p2.other_action = p1.action
        p1.payoff = (Constants.payoff_matrix[p1.action][p1.other_action])
        p2.payoff = (Constants.payoff_matrix[p2.action][p2.other_action])
        p1.other_payoff = p2.payoff
        p2.other_payoff = p1.payoff

        # print((self.round_number,p1.payoff,p2.payoff))

        p1.cum_payoff = sum([p.payoff for p in p1.in_all_rounds()])
        p2.cum_payoff = sum([p.payoff for p in p2.in_all_rounds()])

        # then generate signals
        if p2.action == 'A':  # generate the signal for p1
            if random.random() < Constants.epsilon: # wrong signal
                p1.signal = 'b'
            else:
                p1.signal = 'a'
        elif p2.action == 'B':
            if random.random()<Constants.epsilon: # wrong signal
                p1.signal = 'a'
            else:
                p1.signal = 'b'

        # generate the signal for p2, depending on the two players' actions
        # if p1.action == p2.action:  # the same action, correlated signals
        if p1.action == p1.other_action and p1.action == 'A':  # both chose A, correlated signals
            if random.random()< Constants.gamma: # different signals
                if p1.signal == 'a':
                    p2.signal = 'b'
                else:
                    p2.signal = 'a'
            else: # the same signal
                p2.signal = p1.signal
        else: # different actions, independent signals
            if p1.action == 'A':  # generate the signal for p1
                if random.random() < Constants.epsilon:  # wrong signal
                    p2.signal = 'b'
                else:
                    p2.signal = 'a'
            elif p1.action == 'B':
                if random.random() < Constants.epsilon:  # wrong signal
                    p2.signal = 'a'
                else:
                    p2.signal = 'b'

        p1.other_signal = p2.signal
        p2.other_signal = p1.signal

        # update payoff for Part I in terms of real currency
        p1.participant.vars['real_payoff_PartI'] = p1.cum_payoff * self.session.config['real_world_currency_per_point']
        p2.participant.vars['real_payoff_PartI'] = p2.cum_payoff * self.session.config['real_world_currency_per_point']

        # print((p1.participant.id_in_session,p1.action,p1.payoff,p1.signal,p2.participant.id_in_session,p2.action,p2.payoff,p2.signal))

    def send_message(self):
        p1, p2 = self.get_players()
        p1.other_message = p2.message
        p2.other_message = p1.message
        # print((p1.message,p2.message,p1.other_message,p2.other_message))


class Player(BasePlayer):
    my_id = models.PositiveIntegerField()
    interaction_number = models.PositiveIntegerField()
    round_in_interaction = models.PositiveIntegerField()

    action = models.CharField(
        choices=['A', 'B'],
        doc="""This player's action""",
        widget=widgets.RadioSelect()
    )

    signal = models.CharField(
        choices=['A', 'B'],
        doc="""This player's signal received""",
        widget=widgets.RadioSelect()
    )

    message = models.CharField(
        choices=['a', 'b'],
        doc="""This player's message""",
        widget=widgets.RadioSelect()
    )
    partner_id = models.PositiveIntegerField()
    other_action = models.CharField(choices=['A','B'])
    other_signal = models.CharField(choices=['a','b'])
    other_message = models.CharField(choices=['a','b'])

    cum_payoff = models.CurrencyField()

    def get_partner(self):
        return self.get_others_in_group()[0]

