import random as r
from scipy import special

class Agent(object):
    """This class defines a game playing agent.

    Attributes:
        ID: A unique ID tuple containing (generation, position in generation).
        parent_ID: The unique ID of the agents parent, or None if the agent is
            from the first generation.
        score: A float score associated with the agent
    """

    def __init__(self, max_turns, initial_gift=r.randint(1,), genome_a=0 , genome_b=0, ID=None, 
                 parent_ID=None):
        """Inits Agent.
        """
        self.ID = ID
        self.parent_ID = parent_ID
        self.cash = 100
        self.initial_gift = initial_gift
        self.multipliers = np.ones(max_turns)
        self.genome_a=
        self.genome_b=

    def gift(self, turn, opponent_history , type=0):

        if turn == 0:
            return self.initial_gift
        else:
            relevant_shifts = self.shifts[:turn + 1]
            relevant_multipliers = self.multipliers[:turn + 1]
            relevant_history = opponent_history[:turn + 1]

            linearly_transformed_history = relevant_multipliers * 
                                           (relevant_history - relevant_shifts)

            logistic_input = np.sum(linearly_transformed_history)

            logistic_value = special.expit(logistic_input)

            return logistic_value