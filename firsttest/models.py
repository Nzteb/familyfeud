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

    correctwordlist = ['Apple', 'Banana']



class Subsession(BaseSubsession):

    def creating_session(self):
        #TODO check but I think this is done for every round seperately, so you can use it
        #TODO to distribute the questions to all game rounds of all rounds of the experiment
        alist = []
        alist.append(random.choice(Constants.correctwordlist))
        self.session.vars['correctwordlist'] = alist




class Group(RedwoodGroup):

    def _on_guessingChannel_event(self, event=None, **kwargs):

        print('I went into "_on_guessing_Channel_events_" function...')
        print('I received the guess of the player, the guess is: %s'  %(event.value['guess']))


        #if the word is correct, send it to the correct_guess channel
        if event.value['guess'] in self.session.vars['correctwordlist']:
            self.send('correct_guess', event.value['guess'])
        else: #if the word is not correct send it to the group_guesses channel
            self.send('group_guesses', event.value['guess'])




    def period_length(self):
        print('I went into the "period_length" funcion...')
        return 1000

class Player(BasePlayer):

        def initial_decision(self):
            return 0.5



