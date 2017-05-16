from otree.api import Currency as c, currency_range
from . import models, views
from ._builtin import Page, WaitPage
from .models import Constants
import time
from otree.models_concrete import (PageTimeout, PageCompletion)

from .gto_timeout_page import GTOPage


class Intro(Page):
    timeout_seconds = 100

# if you need to use vars_for_template or before_next_page or is_displayed
# you should either use gto_vars_for_template, gto_before_next_page
# gto_is_displayed or use vars_for_template etc but refer to super

class Demographics(GTOPage):
    general_timeout = True

    form_model = models.Player
    form_fields = ['gender']

    def gto_vars_for_template(self):
        return {'myvar': 'Hello, oh cruel world!'}

class BigFive(GTOPage):
    general_timeout = True

    form_model = models.Player
    form_fields = ['life']

class ThirdPage(GTOPage):
    general_timeout = True

    form_model = models.Player
    form_fields = ['anynumber']
    def gto_is_displayed(self):
        return self.round_number==1

class Results(Page):
    timeout_seconds = 120


page_sequence = [
    Intro,
    Demographics,
    BigFive,
    ThirdPage,
    Results,
]
