import os
from os import environ

import dj_database_url
from boto.mturk import qualification

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
    APPS_DEBUG = False
else:
    DEBUG = True
    APPS_DEBUG = True

# don't share this with anybody.
SECRET_KEY = 'xbsw&0b==_fg)5#4n)ckwgr1-na%c#z=pmt4+13yr!h-x&s=1p'


DATABASES = {
    'default': dj_database_url.config(
        # Rather than hardcoding the DB parameters here,
        # it's recommended to set the DATABASE_URL environment variable.
        # This will allow you to use SQLite locally, and postgres/mysql
        # on the server
        # Examples:
        # export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
        # export DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME

        # fall back to SQLite if the DATABASE_URL env var is missing
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
# REAL_WORLD_CURRENCY_CODE = 'USD'
REAL_WORLD_CURRENCY_CODE = 'AED '
USE_POINTS = True
# POINTS_CUSTOM_NAME = 'tokens'
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 0

# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree','otreeutils']

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            oTree on GitHub
        </a>.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Here are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish.
</p>
"""

ROOMS = [
    {
        'name': 'ssel_b_side',
        'display_name': 'SSEL Desktops B01 - B24 - The B-Sides',
        'participant_label_file': '_rooms/ssel_b_side.txt',
    },
]


# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        # qualification.LocaleRequirement("EqualTo", "US"),
        # qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        # qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        # qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}

EXCHANGE_RATE = 1/150 # change the exchange rate here

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.00,
    'participation_fee': 0.00,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
    {
        'name': 'PD_communication',
        'display_name': "Communication and Cooperation",
        'num_demo_participants': 12,
        'debug': DEBUG,
        'app_sequence': ['my_PD_quiz','my_PD_practice','my_PD','coordination','my_PD_survey','ravens','investment_task','payment_info'],
        'real_world_currency_per_point': EXCHANGE_RATE,
        'participation_fee': 10,
    },
    {
        'name': 'PD_test',
        'display_name': "Repeated prisoner's dilemma_test",
        'num_demo_participants': 4,
        'app_sequence': ['my_PD_practice', 'my_PD', 'coordination', 'ravens',
                         'investment_task' ],
        'real_world_currency_per_point': EXCHANGE_RATE,
        'participation_fee': 10,
    },
    {
        'name': 'PD_practice',
        'display_name': "Practice interaction for repeated prisoner's dilemma",
        'num_demo_participants': 1,
        'app_sequence': ['my_PD_practice'],
        'real_world_currency_per_point': EXCHANGE_RATE,
    },
    {
        'name': 'PD_multiple_interactions',
        'display_name': "Prisoner's Dilemma with multiple interactions",
        'num_demo_participants': 12,
        'debug': DEBUG,
        'app_sequence': ['my_PD'],
        'participation_fee': 10,
        'real_world_currency_per_point': EXCHANGE_RATE,
    },
    {
        'name': 'PD_quiz',
        'display_name': "Quiz questions for Prisoner's Dilemma",
        'num_demo_participants': 1,
        'app_sequence': ['my_PD_quiz', 'my_PD_survey'],
        'real_world_currency_per_point': EXCHANGE_RATE,
    },
    {
        'name': 'Raven',
        'display_name': "Raven's progressive matrix",
        'num_demo_participants': 1,
        'app_sequence': ['ravens'],
        'real_world_currency_per_point': EXCHANGE_RATE,
    },
    {
        'name': 'Investment',
        'display_name': "Investment Task for risk preferences",
        'num_demo_participants': 1,
        'app_sequence': ['investment_task'],
        'real_world_currency_per_point': EXCHANGE_RATE,
    },
    {
        'name': 'Coordination_game',
        'display_name': "Coordination: payoff dominant or risk dominant",
        'num_demo_participants': 4,
        'app_sequence': ['coordination'],
        'real_world_currency_per_point': EXCHANGE_RATE,
    },
    {
        'name': 'my_survey',
        'display_name': "Survey questions for Prisoner's Dilemma",
        'num_demo_participants': 1,
        'app_sequence': ['my_PD_survey'],
        'real_world_currency_per_point': EXCHANGE_RATE,
    },
]

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
