import random as r
from scipy import special
import numpy as np


class Agent(object):
    """This class defines a game playing agent.

    Attributes:
        ID: A unique ID tuple containing (generation, position in generation).
        parent_ID: The unique ID of the agents parent, or None if the agent is
            from the first generation.
        score: A float score associated with the agent
    """

    def __init__(self,  genome_a , genome_b, initial_gift=-1, ID=None, 
                 parent_ID=None,**params):
        """Inits Agent.
        """

        self.ID = ID
        self.parent_ID = parent_ID
        self.cash =0 
        self.score=0
        if initial_gift ==-1: self.initial_gift = r.randint(0,params['ENDOWMENT'][0])
        else:self.initial_gift = initial_gift
        # self.multipliers = np.ones(max_turns) #do we still need this? -a
        self.genome_a=genome_a
        self.genome_b=genome_b

    def gift(self, turn, opponent_history , type=0, **params):
        """
            takes as input the history of the opponents moves as a list (which can be empty)
            then this function turns that list into a vector of length (#actions partner has available)*(size of memory)
            where for each chunk of (#actions partner has available) there is a 1 in the index corresponding to what action was take and 0s elsewhere
            
            this is then multiplied with the (#actions agent has available)X[(#actions partner has available)*(size of memory)] matrix
            the index with the resulting highest legal move is then chosen
            
            type refers to whether the agent is acting as a first mover (investor) or as a second mover(tustee/ contractor)
            0 is the former, 1 the latter 
            
        """
        ENDOWMENT= params['ENDOWMENT']
        MEMORY= params['MEMORY']
        B=params['B']
        
        
        
        if opponent_history != []:
            if type:
                genome=self.genome_b
                genome_partner_shape=self.genome_a.shape
            else:
                genome=self.genome_a
                genome_partner_shape=self.genome_b.shape

            if len(opponent_history) <MEMORY:
                #print opponent_history
                opponent_history=list(opponent_history)+[0 for _ in range(8)] # so that we don't try to access things that don't exist #nvm we apparently pass in extra zeroes
            #print opponent_history
            #print genome.shape
            input_vector=np.transpose(np.matrix([ int(bool(i==opponent_history[(MEMORY*i)/genome.shape[1]])) for i in range(genome.shape[1])]))
            #print input_vector.shape
            output=list(genome*input_vector)
            #print output
            if type:
                result= opponent_history[0]*B+1
                while result >ENDOWMENT[1]*B: # this whole loop just makes sure you can create money if your partner was stingy
                    max_weight= max(output)
                    #print max_weight
                    result=output.index(max_weight)
                    output[result]-=max_weight # to remove that one from the running in case it is too big
                return result    
            else:
                max_weight= max(output)
                #print max_weight
                result=output.index(max_weight)
                return result  
        else:
            # aka the list is empty
            return self.initial_gift
            
        '''
            relevant_shifts = self.shifts[:turn + 1]
            relevant_multipliers = self.multipliers[:turn + 1]
            relevant_history = opponent_history[:turn + 1]

            linearly_transformed_history = relevant_multipliers * 
                                           (relevant_history - relevant_shifts)

            logistic_input = np.sum(linearly_transformed_history)

            logistic_value = special.expit(logistic_input)

            return logistic_value
            ''' # is this okay to get rid of? -a