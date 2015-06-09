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
        self.cash = 0 
        self.score = 0
        

        if initial_gift == -1: 
            self.initial_gift = r.randint(0, params['ENDOWMENT'][0])
        else:
            self.initial_gift = initial_gift

        self.genome_a = genome_a
        self.genome_b = genome_b

    def gift(self, turn, opponent_history , type=0, **params):
        """Takes as input the history of the opponents moves as a list (which 
        can be empty) then this function turns that list into a vector of length 
        (#actions partner has available)*(size of memory) where for each chunk 
        of (#actions partner has available) there is a 1 in the index 
        corresponding to what action was take and 0s elsewhere. This is then 
        multiplied with the (#actions agent has available) X 
        [(#actions partner has available)*(size of memory)] matrix. The index 
        with the resulting highest legal move is then chosen.
        
        Args:
            turn: the current turn
            opponent_history: a list of the opponents previous moves (can be 
                empty)
            type: 0 if the agent is the investor, 1 if the agent is the trustee
            params: 
                endowment: the initial balance of the agent
                memory: how many turns of the history the agent uses to decide
                    its move
                b: the 
        """
        ENDOWMENT= params['ENDOWMENT']
        MEMORY= params['MEMORY']
        B=params['B']
        
        if opponent_history != []:
            if type:
                genome = self.genome_b
                genome_partner_shape = self.genome_a.shape
            else:
                genome=self.genome_a
                genome_partner_shape = self.genome_b.shape
            
            opponent_history_padded=opponent_history
            if len(opponent_history) < MEMORY:
                # print opponent_history
                opponent_history_padded = list(opponent_history) + [-1 for _ in range(MEMORY-len(opponent_history))]
            if len(opponent_history) > MEMORY:
                opponent_history_padded =opponent_history[:MEMORY]
            
            print opponent_history
            print opponent_history_padded
            print genome.shape

            input_vector = np.transpose(np.matrix([int(bool(
                                        i%(genome.shape[1]/MEMORY) == opponent_history_padded[-(MEMORY *i / 
                                        genome.shape[1])])) 
                                        for i in range(genome.shape[1])]))

            print input_vector
            print input_vector.shape
            output=list(genome*input_vector)
            print output    
            #print output

            if type:
                result = opponent_history[0] * B + 1

                # this whole loop just makes sure you can create money if your 
                # partner was stingy
                while result > opponent_history[-1] * B: 
                    max_weight = max(output)
                    print max_weight
                    result = output.index(max_weight)
                    # to remove that one from the running in case it is too big
                    output[result] -= max_weight 
                    print result
                return result    
            else:
                max_weight = max(output)
                print max_weight
                result = output.index(max_weight)
                return result  
        else:
            # aka the list is empty
            return self.initial_gift