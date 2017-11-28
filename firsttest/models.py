from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree_redwood.models import Event, DecisionGroup
from otree_redwood.models import Group as RedwoodGroup
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'firsttest'
    players_per_group = None
    num_rounds = 1



class Subsession(BaseSubsession):

    def creating_session(self):
        # alist = []
        # alist.append(random.choice(['Apple', 'Banana']))
        # alist.append(random.choice(['Soccer', 'Tennis']))
        # self.session.vars['wordlist'] = alist
        pass



class Group(RedwoodGroup):

    def _on_guessingChannel_event(self, event=None, **kwargs):

        print('I went into "_on_guessing_Channel_events_" function...')
        #the guessed value of the event is in form of {word: 'guessed word'}
        print('I received the guess of the player, the guess is: %s'  %(event.value['word']))
        # broadcast the order out to all subjects
        # if event.value['word'] in self.session.vars['wordlist']:
        #     self.send("correct_guess", event.value['word'])

        #send the guess back, in anycase to list it for the other players
        if True:
            self.send('group_guesses', event.value['word'])



    def period_length(self):
        print('I went into the "period_length" funcion...')
        return 1000

class Player(BasePlayer):

        def initial_decision(self):
            return 0.5



