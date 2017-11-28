from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree_redwood.models import Event, DecisionGroup
from otree_redwood.models import Group as RedwoodGroup

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'firsttest'
    players_per_group = None
    num_rounds = 1



class Subsession(BaseSubsession):
    pass


class Group(RedwoodGroup):

    def _on_guessingChannel_event(self, event=None, **kwargs):
        # probably should verify the event.participant has enough balance/units
        # to send the order
        print('I went into "_on_guessing_Channel_events_" function...')
        # broadcast the order out to all subjects
        self.send("correct_guess", event.value)

    def period_length(self):
        print('I went into the "period_length" funcion...')
        return 1000

class Player(BasePlayer):

        def initial_decision(self):
            return 0.5



