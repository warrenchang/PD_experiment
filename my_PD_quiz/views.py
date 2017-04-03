from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

from otreeutils.pages import AllGroupsWaitPage, ExtendedPage, UnderstandingQuestionsPage, APPS_DEBUG


class SomeUnderstandingQuestions(UnderstandingQuestionsPage):
    page_title = 'Quiz questions of Part I'
    set_correct_answers = APPS_DEBUG    # this is the default setting
    # set_correct_answers = False  # do not fill out the correct answers in advance (this is for fast skipping through pages)
    form_model = models.Player
    form_field_n_wrong_attempts = 'understanding_questions_wrong_attempts'
    questions = [
        {
            'question': 'You will be playing with the same participant in all interactions throughout Part I.',
            'options': ['True', 'False'],
            'correct': 'False',
        },
        {
            'question': 'Suppose in a round you choose B, and the other person choose A, your payoff for that round is',
            'options': [150, 130, 30, 5],
            'correct': 150,
            # 'hint': 'You can have a look at Wikipedia!'
        },
        {
            'question': 'Suppose you are in round 6 in an interaction with another participant. The probability that there is a round 7 is',
            'options': [0.95, 0.6, 0.55, 0.4],
            'correct': '0.6',
        },
        {
            'question': "Both you and the other person you are matched with chose A, and you received a random draw 'a'. The probability that the other person also received 'a' random draw a is",
            'options': [0.95, 0.6, 0.55, 0.4],
            'correct': '0.95',
        },
        {
            'question': 'You only know your payoff, but not the choice of the other person at the end of a round.',
            'options': ['True', 'False'],
            'correct': 'False',
        },
        {
            'question': "The random draw you receive depends on the choice of the other person you are matched with.",
            'options': ['True', 'False'],
            'correct': 'True',
        },
        {
            'question': "If you choose A, the probability for the other person to receive a random draw 'a' is always higher than receiving a random draw 'b'.",
            'options': ['True', 'False'],
            'correct': 'True',
        },
        {
            'question': "When you and the other person make the same choice, the probability for you two to receive the same random draw is",
            'options': [0.95, 0.6, 0.55, 0.4],
            'correct': '0.95',
        },
        {
            'question': "You and the other person can send messages about the random draws you received to help each other make decisions.",
            'options': ['True', 'False'],
            'correct': 'True',
        },
        {
            'question': "When you and the other person have different choices, the random draw you receive is independent from the random draw the other person receives.",
            'options': ['True', 'False'],
            'correct': 'True',
        },
    ]


class QuizResults(Page):
    timeout_seconds = 30

    def vars_for_template(self):
        return {
            'quiz_payment': max(10-self.player.understanding_questions_wrong_attempts,0)
        }

    def before_next_page(self):
        self.player.payoff = max(10-self.player.understanding_questions_wrong_attempts,0) / self.session.config['real_world_currency_per_point']
        # payoff are always in points, hence divided by self.session.vars['real_world_currency_per_point']
        self.player.participant.vars['payoff_quiz'] = self.player.payoff.to_real_world_currency(self.session)


page_sequence = [
    SomeUnderstandingQuestions,
    QuizResults,
    AllGroupsWaitPage,
]
