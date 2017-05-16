from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import csv
author = 'Philipp Chapkovski, UZH. Chapkovski@gmail.com'

doc = """
Timeout for several pages at the same time
"""


class Constants(BaseConstants):
    name_in_url = 'bigfive_gto'
    players_per_group = None
    num_rounds = 1
    gto_seconds = 100


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass



class Player(BasePlayer):

    gender = models.CharField(initial=None,
                                choices=['Male', 'Female'],
                                verbose_name='What is your gender?',
                                widget=widgets.RadioSelect())

    life = models.CharField(verbose_name='Tell me what do you think about life in general?',)
    anynumber = models.IntegerField(verbose_name='Choose any number between 0 and 10',)
