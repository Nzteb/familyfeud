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


    #TODO: later on: create different quiz pools for the different rounds, might be the easiest solution to prevent duple questions
    #contains of a list of dictionaries, where each dic is aligned to a round, where each round dics contains a list of question dictionaries
    # the first word in s_i is always the exactly correct solution
    quizload = {'round1':[
                {'question':"Name a Place You Visit Where You Aren't Allowed to Touch Anything",
                   's1': ["Museum gallery",'Museum', 'Gallery', 'Museum gallery'],
                   's2': ['Zoo', 'Animal'],
                   's3': ["Gentleman's club", 'Gentleman club', 'Stripclub', 'Strip club'],
                   's4': ['Baseball'],
                   's5': ['China shop']},

                {'question': "Name an Article of Clothing You Can't Wash in the Washing Machine",
                 's1': ['Shoe','Shoes'],
                 's2': ['Bra'],
                 's3': ['Hat'],
                 's4': ['Coat'],
                 's5': ['Sweater']}]
    }



class Subsession(BaseSubsession):

    def creating_session(self):

        #TODO delete me
        print(' ..I was in creating session ... ')

        #I have to initialize this here, otherwise oTree will look for it
        #TODO .... ?!
        #TODO 12.12.2017 something weird going on here....

        self.session.vars['current_quest_num'] = 1

        for round_num in range(1,11):
            if self.round_number == round_num:
                #at the moment drawing 2 questions for one family feud round
                for question_num in range(1,3):
                    question = random.choice(Constants.quizload['round' + str(round_num)])
                    #ql_11 e.g. means quizload for round 1 question 1
                    #TODO as is, questions could be drawn twice
                    self.session.vars['ql_' + str(round_num) + str(question_num)] = question





class Group(RedwoodGroup):

    def when_all_players_ready(self):
        #initialize the current question to question number 1 when a new family feud round starts
        self.session.vars['current_quest_num'] = 1

        print('when all players ready was called...')
        #send the whole quiz packet to the channel
        self.sendquizload_toplayers()
        return


    #this will triger 'receive_question ()' function in javascript and in javascript the timer will be initialized
    def sendquizload_toplayers(self):
        #reveice the current question number
        quest_num = self.session.vars['current_quest_num']
        #send the correct question to javascript, see the formatting in creating_session
        self.send('questionChannel', self.session.vars['ql_'+ str(self.round_number) + str(quest_num)])
        #increment the current question number, so nexttime you are called you send the next question out

        # TODO delete me:
        print(self.session.vars['current_quest_num'])
        # TODO: 12.12.2017 ok some very weird things are going on here .. the increment works but when the function is
        # TODO called for the second time current_quest_num starts at 1 again... ? so either the creating session function or before players ready
        # TODO must be called? Or is there another reason? Because i cant see why these functions should be called
        # TODO also, the game didnt end despite the fact that period length is set

        #TODO: ok i resetted db again and it actually did finish the game
        #TODO: so the game doesnt end despite the fact that subperiod is set might be false alarm
        #TODO but the incrementing issue remains

        self.session.vars['current_quest_num'] +=1

        #TODO delete me:
        print(self.session.vars['current_quest_num'])

    # if multiple questions are played in one round the first player of every group sends a message to the channel
    # this triggers this function which calls sendquizload to which will send a new question and trigger receive_question in
    # java script, therefore starting a new question
    def _on_questionChannel_event(self, event = None):
        #from javascript the first player in the group requests a question over the question channel
        self.sendquizload_toplayers()

    #reveives all the guesses of the players, decides if guess was right and about points
    #sends processed information back to the players in javascript (e. g. correct guess, wrong guesses)
    def _on_guessingChannel_event(self, event=None):

        #TODO Delete me
        print('I went into "_on_guessing_Channel_events_" function...')
        print('I received the guess of the player, the guess is: %s' % (event.value['guess']))

        #the guess that was send from a player
        guess = event.value['guess'].lower()
        # the the current question (dictionaire)
        question = self.session.vars['ql_' + str(self.round_number) + str(self.session.vars['current_quest_num'])]
        good_guess = False
        # check if the guess is correct, if yes send it, together with the answernum, to correct_guess channel
        for answernum in ['s1', 's2', 's3', 's4', 's5']:
            if guess in list(map(lambda x: x.lower(), question[answernum])): # e. g. question[s1] is a list with all the solutions for the correct word 1 of the current question
                good_guess = True
                self.send('correct_guess', {'correctguess': question[answernum][0], #send the exactly correct answer back, which is the 0 element of the list
                                            'whichword': answernum})
                break
        if good_guess == False: #word was not right, send it to the usual group channel so it can be displayed on the right
                self.send('group_guesses', guess)







    def period_length(self):
        print('I went into the "period_length" funcion...')
        return 90

class Player(BasePlayer):

        def initial_decision(self):
            return 0.5





