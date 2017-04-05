from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from otreeutils.surveys import create_player_model_for_survey

author = 'Huanren Zhang'

doc = """
Survey questions
"""


class Constants(BaseConstants):
    name_in_url = 'my_PD_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


GENDER_CHOICES = (
    ('female', 'Female'),
    ('male', 'Male'),
    # ('no_answer', 'Prefer not to answer'),
)

YESNO_CHOICES = (
    ('yes', 'Yes'),
    ('no', 'No'),
)


# define survey questions per page
# for each page define a page title and a list of questions
# the questions have a field name, a question text (input label), and a field type (model field class)
SURVEY_DEFINITIONS = (
    {
        'page_title': 'Survey Questions - Page 1',
        'survey_fields': [
            ('age', {   # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'How old are you?',   # survey question
                'field': models.PositiveIntegerField(min=16, max=100),  # the same as in normal oTree model field definitions
            }),
            ('gender', {
                'text': 'What is  your gender.',
                'field': models.CharField(choices=GENDER_CHOICES),
            }),
            ('birth_place', {
                'text': 'Where were you born?',
                'field': models.CharField(choices=['Middle East', 'China, Taiwan, Hong Kong, or Macau',
                                                   'East Asia', 'South-East Asia', 'South Asia', 'Other Asia',
                                                   'United States','Canada','Latin America',
                                                   'Australia/New Zealand', 'Other Pacific Nation', 'United Kingdom',
                                                   'Eastern Europe', 'Southern Europe', 'Northern Europe',
                                                   'Other Europe','Africa'
                                                   ]),
            }),
        ]
    },
    {
        'page_title': 'Survey Questions - Page 2',
        'survey_fields': [
            ('religion', {   # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'What religion are you?',   # survey question
                'field':  models.CharField(choices=['Muslim',  'Christian', 'Buddhism','Hindu',
                                                    'None','Other','Rather not to say'
                                                    ]),
            }),
            ('reg_importance', {
                'text': 'How important do you consider religion in your daily life?',
                'field': models.PositiveIntegerField(
                    choices=[
                        [4, 'Very important'],
                        [3, 'Somewhat important'],
                        [2, 'A little important'],
                        [1, 'Not at all important'],
                    ]),
            }),
        ]
    },
    {
        'page_title': 'Survey Questions - Page 3',
        'survey_fields': [
            ('school_year', {   # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'Which year are you at the university?',   # survey question
                'field':  models.CharField(choices=[ '1st year', '2nd year', '3rd year', '4th or more', 'Graduate student'
                                                     ]),
            }),
            ('major', {  # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'What is your major?',  # survey question
                'field': models.CharField(choices=['Economics', 'Management', 'Social Science', 'Science',
                                                   'Engineering', 'Art or Humanity'
                                                   ]),
            }),
            ('gpa', {
                'text': 'What is your GPA at the university?',
                'field': models.CharField(choices=[ 'Between 3.5-4', 'Between 3-3.49', 'Between 2.5-2.99',
                                                    'Between 2-2.49', 'Below 2'
                                                    ]),
            }),
        ]
    },
    # {
    #     'page_title': 'Survey Questions - Page 4',
    #     'survey_fields': [
    #         ('importance_self',
    #          {  # field name (which will also end up in your "Player" class and hence in your output data)
    #              'text': 'When making your choice in Part I, how important it is to consider how this choice may affect your earnings in this interaction?',
    #              # survey question
    #              'field': models.PositiveIntegerField(
    #                  choices=[
    #                      [1, '1. Very unimportant'],
    #                      [2, '2. Moderately unimportant'],
    #                      [3, '3. Neutral'],
    #                      [4, '4. Moderately important'],
    #                      [5, '5. Very important']
    #                  ]),
    #          }),
    #         ('importance_other',
    #          {  # field name (which will also end up in your "Player" class and hence in your output data)
    #              'text': "When making your choice in Part I, how important it is to consider how this choice may affect the other person's earnings in this interaction?",
    #              # survey question
    #              'field': models.PositiveIntegerField(
    #                  choices=[
    #                      [1, '1. Very unimportant'],
    #                      [2, '2. Moderately unimportant'],
    #                      [3, '3. Neutral'],
    #                      [4, '4. Moderately important'],
    #                      [5, '5. Very important']
    #                  ]),
    #          }),
    #         ('importance_total',
    #          {  # field name (which will also end up in your "Player" class and hence in your output data)
    #              'text': 'When making your choice in Part I, how important it is to consider how this choice may lead to higher total earnings for you and the other person in this interaction?',
    #              # survey question
    #              'field': models.PositiveIntegerField(
    #                  choices=[
    #                      [1, '1. Very unimportant'],
    #                      [2, '2. Moderately unimportant'],
    #                      [3, '3. Neutral'],
    #                      [4, '4. Moderately important'],
    #                      [5, '5. Very important']
    #                  ]),
    #          }),
    #     ]
    # },
    {
        'page_title': 'Survey Questions - Page 4',
        'survey_fields': [
            ('satisfaction1',
             {  # field name (which will also end up in your "Player" class and hence in your output data)
                 'text': 'On a scale from 1 to 5, please indicate, overall, how dissatisfied/satisfied you are with the outcomes of Part I',
                 # survey question
                 'field': models.PositiveIntegerField(
                     choices=[
                         [1, '1. Very dissatisfied'],
                         [2, '2. Moderately dissatisfied'],
                         [3, '3. Neutral'],
                         [4, '4. Moderately satisfied'],
                         [5, '5. Very satisfied']
                     ]),
             }),
            ('strategy1', {  # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'Describe your strategy for Part I: How did you make the choice? Did you base your choice on the signal you received? How did you choose the message to send? How did you base your choice on the messages you sent or received.',
            # survey question
                'field': models.TextField(),
            }),
            ('strategy_again1',
             {  # field name (which will also end up in your "Player" class and hence in your output data)
                 'text': 'What would you do differently if you can do Part I again?',
                 'field': models.TextField(),
             }),

        ]
    },
    {
        'page_title': 'Survey Questions - Page 4',
        'survey_fields': [
            ('satisfaction1',
             {  # field name (which will also end up in your "Player" class and hence in your output data)
                 'text': 'On a scale from 1 to 5, please indicate, overall, how dissatisfied/satisfied you are with the outcomes of Part I',
                 # survey question
                 'field': models.PositiveIntegerField(
                     choices=[
                         [1, '1. Very dissatisfied'],
                         [2, '2. Moderately dissatisfied'],
                         [3, '3. Neutral'],
                         [4, '4. Moderately satisfied'],
                         [5, '5. Very satisfied']
                     ]),
             }),
            ('strategy1', {  # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'Describe your strategy for Part I: How did you make the choice? Did you base your choice on the signal you received or the other person receive?',
                # survey question
                'field': models.TextField(),
            }),
            ('strategy_again1',
             {  # field name (which will also end up in your "Player" class and hence in your output data)
                 'text': 'What would you do differently if you can do Part I again?',
                 'field': models.TextField(),
             }),

        ]
    },
    {
        'page_title': 'Survey Questions - Page 5',
        'survey_fields': [
            ('satisfaction2',
             {  # field name (which will also end up in your "Player" class and hence in your output data)
                 'text': 'On a scale from 1 to 5, please indicate, overall, how dissatisfied/satisfied you are with the outcomes of Part II',
                 # survey question
                 'field': models.PositiveIntegerField(
                     choices=[
                         [1, '1. Very dissatisfied'],
                         [2, '2. Moderately dissatisfied'],
                         [3, '3. Neutral'],
                         [4, '4. Moderately satisfied'],
                         [5, '5. Very satisfied']
                     ]),
             }),
            ('strategy2', {  # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'Describe your strategy for Part II. How did you make your decision?',
                'field': models.TextField(),
            }),
            ('strategy_again2',
             {  # field name (which will also end up in your "Player" class and hence in your output data)
                 'text': 'What would you do differently if you can do Part II again?',
                 'field': models.TextField(),
             }),

        ]
    },
    {
        'page_title': 'Survey Questions - Page 6',
        'survey_fields': [
            ('difficulty',
             {  # field name (which will also end up in your "Player" class and hence in your output data)
                 'text': 'Do you consider the first two parts of the experiment easy to understand and follow?',
                 'field': models.PositiveIntegerField(
                     choices=[
                         [1, '1. Very easy'],
                         [2, '2. Easy'],
                         [3, '3. Moderate'],
                         [4, '4. Difficult'],
                         [5, '5. Very difficult']
                     ]),
             }),
            ('experiment_like', {  # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'What you like/dislike about the experiment? Which part is hard to follow?',
                'field': models.TextField(),
            }),

        ]
    },
)

# now dynamically create the Player class from the survey definitions
Player = create_player_model_for_survey('my_PD_survey.models', SURVEY_DEFINITIONS)
