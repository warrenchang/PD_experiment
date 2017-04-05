from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Huanren Zhang'

doc = """
Practice rounds for infinitely repeated "Prisoner's Dilemma" with private monitoring.
"""


class Constants(BaseConstants):
    name_in_url = 'PD_practice'
    players_per_group = None

    num_rounds = 5
    number_sequence = [ 5,  4,  2,  6,  9]
    interactions = [0,0,0,0,0,0]
    round_in_interactions = [1,2,3,4,5]
    interaction_length = [6]
    num_interactions = 1


    epsilon = 0.45
    gamma = 0.05

    instructions_template = 'my_PD_practice/Instructions.html'

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
    pass


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
    payoff0 = models.CurrencyField() # define payoff0, record payoff but do not count for final payment

    def get_partner(self):
        return self.get_others_in_group()[0]

    def interact(self):
        # first calculate payoff
        if self.action == 'A':
            self.other_action = 'A'
        else:
            self.other_action = random.choice(['A','B'])
        self.payoff0 = (Constants.payoff_matrix[self.action][self.other_action])
        self.other_payoff = (Constants.payoff_matrix[self.other_action][self.action])

        self.cum_payoff = sum([p.payoff0 for p in self.in_all_rounds()])

        # then generate signals
        if self.other_action == 'A':  # generate the signal for self
            if random.random() < Constants.epsilon: # wrong signal
                self.signal = 'b'
            else:
                self.signal = 'a'
        elif self.other_action == 'B':
            if random.random()<Constants.epsilon: # wrong signal
                self.signal = 'a'
            else:
                self.signal = 'b'

        # generate the signal for p2, depending on the two players' actions
        # if self.action == self.other_action:  # the same action, correlated signals
        if self.action == self.other_action and self.action == 'A':  # both chose A, correlated signals
            if random.random()< Constants.gamma: # different signals
                if self.signal == 'a':
                    self.other_signal = 'b'
                else:
                    self.other_signal = 'a'
            else: # the same signal
                self.other_signal = self.signal
        else: # different actions, independent signals
            if self.action == 'A':  # generate the signal for the opponent
                if random.random() < Constants.epsilon:  # wrong signal
                    self.other_signal = 'b'
                else:
                    self.other_signal = 'a'
            elif self.action == 'B':
                if random.random() < Constants.epsilon:  # wrong signal
                    self.other_signal = 'a'
                else:
                    self.other_signal = 'b'

    def send_message(self):
        if self.action == 'A' and self.action == self.other_action:
            self.other_message = self.other_signal
        else:
            self.other_message = random.choice(['a','b'])

