from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

from otreeutils.surveys import SurveyPage, setup_survey_pages


class StartPage(Page):
    def is_displayed(self):
        if self.round_number == 1:
            print('This is the start of PD survey')
        print(self.participant.vars)
        return self.round_number == 1


# class SurveyIntro(Page):
#     pass

# let's create the survey pages here
# unfortunately, it's not possible to create them dynamically

class SurveyPage1(SurveyPage):
    pass


class SurveyPage2(SurveyPage):
    pass


class SurveyPage3(SurveyPage):
    pass

class SurveyPage4(SurveyPage):
    pass


class SurveyPage5(SurveyPage):
    pass


class SurveyPage6(SurveyPage):
    pass

# Create a list of survey pages.
# The order is important! The survey questions are taken in the same order
# from the SURVEY_DEFINITIONS in models.py

survey_pages = [
    SurveyPage1,
    SurveyPage2,
    SurveyPage3,
    SurveyPage4,
    SurveyPage5,
    SurveyPage6,
]

# Common setup for all pages (will set the questions per page)
setup_survey_pages(models.Player, survey_pages)

page_sequence = [
    StartPage,
    # SurveyIntro,
]

# add the survey pages to the page sequence list
page_sequence.extend(survey_pages)

