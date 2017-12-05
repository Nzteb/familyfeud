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

    #the first word in s_i is always the exactly correct solution
    quizload = [{'question':"Name a Place You Visit Where You Aren't Allowed to Touch Anything",
                   's1': ["museum gallery",'museum', 'gallery', 'museum gallery'],
                   's2': ['zoo', 'animal'],
                   's3': ["gentleman's club", 'gentleman club', 'stripclub', 'strip club'],
                   's4': ['baseball'],
                   's5': ['china shop']},

                {'question': "Name an Article of Clothing You Can't Wash in the Washing Machine",
                 's1': ['shoe','shoes'],
                 's2': ['bra'],
                 's3': ['hat'],
                 's4': ['coat'],
                 's5': ['sweater']}]



class Subsession(BaseSubsession):

    def creating_session(self):
        #TODO check but I think this is done for every round seperately, so you can use it
        #TODO to distribute the questions to all game rounds of all rounds of the experiment

        question = random.choice(Constants.quizload)
        #each quizload_i shall only hold one question so there shouldnt be ambiguity
        self.session.vars['quizload1'] = question
        #TODO add quizload 2-5 for the other 4 familifeud subrounds of one game round




class Group(RedwoodGroup):

    #TODO: when I enter the session with a player it does not wait for the other players to start yet?
    #TODO but at least the function is called, this is good I suppose
    def when_all_players_ready(self):
        print('when all players ready was called...')
        #send the whole quiz packet to the channel
        self.send('questionChannel', self.session.vars['quizload1'])
        return


    def _on_guessingChannel_event(self, event=None, **kwargs):

        #TODO Delete me
        print('I went into "_on_guessing_Channel_events_" function...')
        print('I received the guess of the player, the guess is: %s' % (event.value['guess']))

        #the guess that was send from a player
        guess = event.value['guess'].lower()
        # the the current question (dictionaire)
        question = self.session.vars['quizload1']

        good_guess = False
        for answernum in ['s1', 's2', 's3', 's4', 's5']:
            #check if the guess is correct, if yes send it, together with the answernum, to correct_guess channel
            if guess in question[answernum]:
                good_guess = True
                self.send('correct_guess', {'correctguess': question[answernum][0].capitalize(), #send the exactly correct answer back
                                            'whichword': answernum})
                break
        if good_guess == False: #word was not right, send it to the usual group channel so it can be displayed on the right
                self.send('group_guesses', guess)







    def period_length(self):
        print('I went into the "period_length" funcion...')
        return 160

class Player(BasePlayer):

        def initial_decision(self):
            return 0.5





