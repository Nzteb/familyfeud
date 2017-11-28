from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree_redwood.models import Event, DecisionGroup

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


class Group(DecisionGroup):

    def _on_guessing_event(self, event=None, **kwargs):
        # probably should verify the event.participant has enough balance/units
        # to send the order
        print('heloooooooooooooo')
        # broadcast the order out to all subjects
        self.send("correct_guess", event.value)

    def period_length(self):
        print(' i was here......................')
        return 1000

class Player(BasePlayer):

        def initial_decision(self):
            return 0.5



