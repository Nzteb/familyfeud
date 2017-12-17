from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from otree_redwood.models import Group as RedwoodGroup
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'firsttest'
    players_per_group = None
    num_rounds = 2
    questions_per_round = 1
    secs_per_question = 20
    wait_between_question = 4



    quizload = [
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
                 's5': ['Sweater']}
    ]



class Subsession(BaseSubsession):

    #remember: this function is seperately called for every oTree round when one clicks creating session
    def creating_session(self):

        #copy the list of questions to alter it when drawing from it
        quizload = Constants.quizload.copy()
        questions_per_round = Constants.questions_per_round

        # distribute all the questions randomly over the rounds and subquestions (if multiple questions per round)
        # a question cannot be drawn twice for the whole game
        for round_num in range(1,Constants.num_rounds+1):
            if self.round_number == round_num:
                for question_num in range(1,questions_per_round+1):
                    question = random.choice(quizload)
                    quizload.remove(question)
                    # hold the quizload of the question in session.vars to acces later
                    # ql_11 e.g. means quizload for round 1 question 1
                    self.session.vars['ql_' + str(round_num) + str(question_num)] = question




class Group(RedwoodGroup):

    current_quest_num = models.IntegerField()

    def when_all_players_ready(self):
        #initialize the current question to question number 1 when a new family feud round starts
        self.current_quest_num = 1
        #TODO delete me..
        print('when all players ready was called...')
        #send the whole quiz packet (one question) to the channel
        self.sendquizload_toplayers()
        return


    # this will triger 'receive_question ()' function in javascript and in javascript the timers will be initialized
    # the function is called at the beginning from when_all_players_ready and under multiple questions when requested from a player through questionChannel
    def sendquizload_toplayers(self):
        #send the correct question to javascript, see the formatting in creating_session
        self.send('questionChannel', self.session.vars['ql_'+ str(self.round_number) + str(self.current_quest_num)])
        #increment the current question number, so nexttime you are called you send the next question out
        self.current_quest_num +=1
        #TODO: You need save() here, otherwise the incrementing does not have permanent effect and weird things happen
        #TODO: see the oTree Redwood doc Group.save()
        self.save()


    # if multiple questions in a round this will be triggered from each first player in the group by the channel; e. g. the player requests a new question
    def _on_questionChannel_event(self, event = None):
        #send a new question back
        self.sendquizload_toplayers()

    #reveives all the guesses of the players, decides if guess was right and shall calculate points
    #sends processed information back to the players in javascript (e. g. correct guess, wrong guesses)
    def _on_guessingChannel_event(self, event=None):
        #TODO Delete me
        print('I went into "_on_guessing_Channel_events_" function...')
        print('I received the guess of the player, the guess is: %s' % (event.value['guess']))

        #the guess that was send from a player
        guess = event.value['guess'].lower()

        # the the current question (dictionaire)
        question = self.session.vars['ql_' + str(self.round_number) + str(self.current_quest_num-1)] # you need the minus 1 because curr_quest is immediately in
                                                                                                     # -cremented after sending the question out, so the current is actually curr_quest-1
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
        #TODO delete me
        print('I went into the "period_length" funcion...')
        # determine time in seconds before the game is left and the next page is displayed
        # TODO: could it be that javascript is slower and the game is aborted before it is finished?
        return (Constants.questions_per_round) * ((Constants.secs_per_question + Constants.wait_between_question)-1) # TODO: with the minus one we assume
                                                                                                                     # that javascript does not slow down at all
                                                                                                                     # then we abort the game 1 second before the
                                                                                                                     # next question is displayed


class Player(BasePlayer):

        def initial_decision(self):
            return 0.5





