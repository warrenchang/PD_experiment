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
    name_in_url = 'my_PD'
    players_per_group = 2

    # num_rounds = 100
    # number_sequence = [ 2,  4,  3, 10,  4,  9,  3, 10,  7,  6,  4,  4,  3,  5,  1,  9,  6,
    #                     3,  4, 10, 10,  2,  3,  8,  5,  7,  8,  3,  9,  7,  4,  7,  4,  7,
    #                     5,  9,  6,  8, 10,  7,  5,  4,  1,  2,  6,  9,  2,  5,  1, 10,  3,
    #                     2,  8, 10,  2,  2,  9,  5,  3,  7,  1,  7,  8,  3,  3,  4, 10,  6,
    #                     10,  6,  4,  4,  2,  5,  9, 10,  1, 10,  5,  8,  2,  1,  8,  3,  2,
    #                     7,  3,  1,  6,  7,  5,  2, 10,  4,  1,  5,  9,  9,  7,  8]
    # interactions = [1,  1,  1,  1,  2,  2,  3,  3,  4,  5,  5,  5,  5,  5,  5,  5,  6,
    #                 6,  6,  6,  7,  8,  8,  8,  9,  9, 10, 11, 11, 12, 13, 13, 14, 14,
    #                 15, 15, 16, 16, 17, 18, 19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 21,
    #                 21, 21, 22, 23, 23, 23, 24, 24, 24, 25, 25, 26, 27, 27, 27, 27, 28,
    #                 28, 29, 29, 29, 29, 29, 29, 30, 31, 31, 32, 32, 33, 33, 33, 34, 34,
    #                 34, 35, 35, 35, 35, 36, 36, 36, 37, 37, 37, 37, 38, 39, 40 ]
    # round_in_interactions = [1, 2, 3, 4, 1, 2, 1, 2, 1, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 1, 1, 2,
    #                          3, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 3, 4, 5, 6,
    #                          1, 2, 3, 4, 1, 2, 3, 1, 1, 2, 3, 1, 2, 3, 1, 2, 1, 1, 2, 3, 4, 1, 2,
    #                          1, 2, 3, 4, 5, 6, 1, 1, 2, 1, 2, 1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 1, 2,
    #                          3, 1, 2, 3, 4, 1, 1, 1 ]
    # interaction_length = [4, 2, 2, 1, 7, 4, 1, 3, 2, 1, 2, 1, 2, 2, 2, 2, 1, 1, 6, 4, 3, 1, 3,
    #                       3, 2, 1, 4, 2, 6, 1, 2, 2, 3, 3, 4, 3, 4, 1, 1, 1]
    # num_interactions = 40

    number_sequence = [ 2,  4,  3, 10,  4,  9,  3, 10,  7,  6,  4,  4,  3,  5,  1,  9,  6,
        3,  4, 10, 10,  2,  3,  8,  5,  7,  8,  3,  9,  7,  4,  7,  4,  7,
        5,  9,  6,  8, 10,  7,  5,  4,  1,  2,  6,  9,  2,  5,  1, 10,  3,
        2,  8, 10,  2,  2,  9,  5,  3,  7,  1,  7,  8,  3,  3,  4, 10,  6,
       10,  6,  4,  4,  2,  5,  9, 10]
    interactions = [1,  1,  1,  1,  2,  2,  3,  3,  4,  5,  5,  5,  5,  5,  5,  5,  6,
        6,  6,  6,  7,  8,  8,  8,  9,  9, 10, 11, 11, 12, 13, 13, 14, 14,
       15, 15, 16, 16, 17, 18, 19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 21,
       21, 21, 22, 23, 23, 23, 24, 24, 24, 25, 25, 26, 27, 27, 27, 27, 28,
       28, 29, 29, 29, 29, 29, 29, 30]
    round_in_interactions = [1, 2, 3, 4, 1, 2, 1, 2, 1, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 1, 1, 2,
       3, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 3, 4, 5, 6,
       1, 2, 3, 4, 1, 2, 3, 1, 1, 2, 3, 1, 2, 3, 1, 2, 1, 1, 2, 3, 4, 1, 2,
       1, 2, 3, 4, 5, 6, 1]
    interaction_length = [4, 2, 2, 1, 7, 4, 1, 3, 2, 1, 2, 1, 2, 2, 2, 2, 1, 1, 6, 4, 3, 1, 3,
       3, 2, 1, 4, 2, 6, 1]
    num_rounds = 76
    # num_rounds = 8 # change num_rounds for testing purpose, but need to make sure that number_sequence
    num_interactions = interactions[num_rounds-1]


    # num_rounds = 3
    # number_sequence = [ 8,  6,  9]
    # interactions = [1,2,2]
    # round_in_interactions = [1,1,2]
    # interaction_length = [1, 2]
    # num_interactions = 2


    epsilon = 0.45
    gamma = 0.05

    instructions_template = 'my_PD/Instructions.html'

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

