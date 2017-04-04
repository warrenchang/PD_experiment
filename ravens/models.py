from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Huanren Zhang'

doc = """
Raven's progressive matrices test measuring cognitive ability
"""


class Constants(BaseConstants):
    name_in_url = 'ravens'
    players_per_group = None
    num_rounds = 10
    answer_keys = [4,2,2,1,5,7,3,6,4,5]
    instructions_template = 'ravens/Instructions.html'


class Subsession(BaseSubsession):
    def before_session_starts(self):
        # this is run before the start of every round
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars['payoff_ravens'] = 0


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    answer = models.PositiveIntegerField(choices=[1,2,3,4,5,6,7,8])
    ans_correct = models.BooleanField()

