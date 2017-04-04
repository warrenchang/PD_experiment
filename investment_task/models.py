from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Huanren Zhang'

doc = """
Investment task that measures risk preferences. Similar to Gneezy and Potter (1997) and Eckel and Grossman (2002,2008)
"""


class Constants(BaseConstants):
    name_in_url = 'investment_task'
    players_per_group = None
    num_rounds = 1

    instructions_template = 'investment_task/Instructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    amount_invested = models.PositiveIntegerField(
        choices=[
            [0, "Not invest"],
            [1, "Invest 1 to A"],
            [2, "Invest 2 to A"],
            [3, "Invest 3 to A"],
            [4, "Invest 4 to A"],
            [5, "Invest 5 to A"],
            [6, "Invest 6 to A"],
            [7, "Invest 7 to A"],
            [8, "Invest 8 to A"],
            [9, "Invest 9 to A"],
            [10, "Invest 10 to A"],
            [11, "Invest 11 to A"],
            [12, "Invest 12 to A"],
            [13, "Invest 13 to A"],
            [14, "Invest 14 to A"],
            [15, "Invest 15 to A"],
            [16, "Invest 16 to A"],
            [17, "Invest 17 to A"],
            [18, "Invest 18 to A"],
            [19, "Invest 19 to A"],
            [20, "Invest 20 to A"],
            [21, "Invest to B"],
        ]
    )
    success = models.BooleanField()
    random_draw = models.IntegerField()
